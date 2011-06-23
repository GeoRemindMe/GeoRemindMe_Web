#!/usr/bin/python2.5
#
# Copyright 2009 Roman Nurik
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines the GeoModel class for running basic geospatial queries on
single-point geographic entities in Google App Engine.

TODO(romannurik): document how bounding box and proximity queries work.
"""

__author__ = 'api.roman.public@gmail.com (Roman Nurik)'

import copy
import logging

from google.appengine.ext import db

import geocell
import geomath
import geotypes
import util

DEBUG = False


def default_cost_function(num_cells, resolution):
  """The default cost function, used if none is provided by the developer."""
  return 1e10000 if num_cells > pow(geocell._GEOCELL_GRID_SIZE, 2) else 0


class GeoModel(db.Model):
  """A base model class for single-point geographically located entities.

  Attributes:
    location: A db.GeoPt that defines the single geographic point
        associated with this entity.
  """
  location = db.GeoPtProperty()
  location_geocells = db.StringListProperty()

  def update_location(self):
    """Syncs underlying geocell properties with the entity's location.

    Updates the underlying geocell properties of the entity to match the
    entity's location property. A put() must occur after this call to save
    the changes to App Engine."""
    if self.location:
      max_res_geocell = geocell.compute(self.location)
      self.location_geocells = [max_res_geocell[:res]
                                for res in
                                range(1, geocell.MAX_GEOCELL_RESOLUTION + 1)]
    else:
      self.location_geocells = []

  @staticmethod
  def bounding_box_fetch(query, bbox, max_results=1000,
                         cost_function=None):
    """Performs a bounding box fetch on the given query.

    Fetches entities matching the given query with an additional filter
    matching only those entities that are inside of the given rectangular
    bounding box.

    Args:
      query: A db.Query on entities of this kind that should be additionally
          filtered by bounding box and subsequently fetched.
      bbox: A geotypes.Box indicating the bounding box to filter entities by.
      max_results: An optional int indicating the maximum number of desired
          results.
      cost_function: An optional function that accepts two arguments:
          * num_cells: the number of cells to search
          * resolution: the resolution of each cell to search
          and returns the 'cost' of querying against this number of cells
          at the given resolution.

    Returns:
      The fetched entities.

    Raises:
      Any exceptions that google.appengine.ext.db.Query.fetch() can raise.
    """
    # TODO(romannurik): Check for GqlQuery.
    results = []

    if cost_function is None:
      cost_function = default_cost_function
    query_geocells = geocell.best_bbox_search_cells(bbox, cost_function)

    results = util.async_in_query_fetch(
        query, 'location_geocells', query_geocells, max_results=max_results,
        debug=DEBUG)

    if DEBUG:
      logging.debug(('GeoModel Bounds Query: '
                     'Looked in %d geocells') %
                    (len(query_geocells),))

    # In-memory filter.
    return [entity for entity in results if
        entity.location.lat >= bbox.south and
        entity.location.lat <= bbox.north and
        entity.location.lon >= bbox.west and
        entity.location.lon <= bbox.east]

  @staticmethod
  def proximity_fetch(query, center, max_results=10, max_distance=0,
                      start_resolution=geocell.MAX_GEOCELL_RESOLUTION):
    """Performs a proximity/radius fetch on the given query.

    Fetches at most max_results entities matching the given query,
    ordered by ascending distance from the given center point, and optionally
    limited by the given maximum distance.

    This method uses a greedy algorithm that starts by searching high-resolution
    geocells near the center point and gradually looking in lower and lower
    resolution cells until max_results entities have been found matching the
    given query and no closer possible entities can be found.

    Args:
      query: A db.Query on entities of this kind.
      center: A geotypes.Point or db.GeoPt indicating the center point around
          which to search for matching entities.
      max_results: An int indicating the maximum number of desired results.
          The default is 10, and the larger this number, the longer the fetch
          will take.
      max_distance: An optional number indicating the maximum distance to
          search, in meters.
      start_resolution: An optional number indicating the geocell resolution
          to begin the search at. Larger values will result in longer response
          times on average, but are more efficient for extremely dense data.
          The default is geocell.MAX_GEOCELL_RESOLUTION

    Returns:
      The fetched entities, sorted in ascending order by distance to the search
      center.

    Raises:
      Any exceptions that google.appengine.ext.db.Query.fetch() can raise.
    """
    # TODO(romannurik): check for GqlQuery
    results = []

    searched_cells = set()

    # The current search geocell containing the lat,lon.
    cur_containing_geocell = geocell.compute(center, start_resolution)

    # The currently-being-searched geocells.
    # NOTES:
    #     * Start with max possible.
    #     * Must always be of the same resolution.
    #     * Must always form a rectangular region.
    #     * One of these must be equal to the cur_containing_geocell.
    cur_geocells = [cur_containing_geocell]

    closest_possible_next_result_dist = 0
   
    sorted_edge_dirs = [(0,0)]
    sorted_edge_distances = [0]

    # Assumes both a and b are lists of (entity, dist) tuples, *sorted by dist*.
    # NOTE: This is an in-place merge, and there are guaranteed
    # no duplicates in the resulting list.
    def _merge_results_in_place(a, b):
      util.merge_in_place(a, b,
                        cmp_fn=lambda x, y: cmp(x[1], y[1]),
                        dup_fn=lambda x, y: x[0].key() == y[0].key())
   
    def _first_horz(edges):
      return [x for x in edges if x[0] != 0][0]
   
    def _first_vert(edges):
      return [x for x in edges if x[0] == 0][0]

    while cur_geocells:
      cur_geocells_unique = list(set(cur_geocells).difference(searched_cells))
      cur_resolution = len(cur_geocells[0])

      # Run query on the next set of geocells.
      new_results = util.async_in_query_fetch(
          query, 'location_geocells', cur_geocells_unique,
          max_results=max_results * len(cur_geocells_unique),
          debug=DEBUG)

      # Update results and sort.
      searched_cells.update(cur_geocells)

      # Begin storing distance from the search result entity to the
      # search center along with the search result itself, in a tuple.
      new_results = [(entity, geomath.distance(center, entity.location))
                     for entity in new_results]
      new_results = sorted(new_results, lambda dr1, dr2: cmp(dr1[1], dr2[1]))
      new_results = new_results[:max_results]

      # Merge new_results into results or the other way around, depending on
      # which is larger.
      if len(results) > len(new_results):
        _merge_results_in_place(results, new_results)
      else:
        _merge_results_in_place(new_results, results)
        results = new_results

      results = results[:max_results]

      if DEBUG:
        logging.debug(('GeoModel Proximity Query: '
                       'Have %d results') %
                      (len(results),))
     
      if len(results) >= max_results:
        if DEBUG:
          logging.debug(('GeoModel Proximity Query: '
                         'Wanted %d results, ending search') %
                        (max_results,))
        break
     
      # Determine the next set of geocells to search.
      sorted_edge_dirs, _ = \
          util.distance_sorted_edges(util.max_box(cur_geocells), center)

      if len(results) == 0 or len(cur_geocells) == 4:
        # Either no results (in which case we optimize by not looking at
        # adjacents, go straight to the parent) or we've searched 4 adjacent
        # geocells, in which case we should now search the parents of those
        # geocells.
        cur_containing_geocell = cur_containing_geocell[:-1]
        cur_geocells = list(set([cell[:-1] for cell in cur_geocells]))
       
        if not cur_geocells or not cur_geocells[0]:
          break  # Done with search, we've searched everywhere.
       
        if len(cur_geocells) == 2:
          # There are two parents for the 4 just-searched cells; get 2
          # perpendicular adjacent parents to search a full set of 4 cells.
          perp_dir = (_first_vert(sorted_edge_dirs)
                      if geocell.collinear(cur_geocells[0],
                                           cur_geocells[1], False)
                      else _first_horz(sorted_edge_dirs))
         
          cur_geocells.extend(
              filter(lambda x: x is not None, [
                     geocell.adjacent(cur_geocells[0], perp_dir),
                     geocell.adjacent(cur_geocells[1], perp_dir)]))

      elif len(cur_geocells) == 1:
        # Searched one geocell, now search its 3 adjacents.
        horz_dir = _first_horz(sorted_edge_dirs)
        vert_dir = _first_vert(sorted_edge_dirs)
        diag_dir = (horz_dir[0], vert_dir[1])
       
        cur_geocells.extend(
            filter(lambda x: x is not None, [
                   geocell.adjacent(cur_geocells[0], horz_dir),
                   geocell.adjacent(cur_geocells[0], vert_dir),
                   geocell.adjacent(cur_geocells[0], diag_dir)]))

      # Stop the search if the next closest possible search result is farther
      # than max_distance or, if we have max_results results already, farther
      # than the last result.
      _, sorted_edge_distances = \
          util.distance_sorted_edges(util.max_box(cur_geocells), center)
      closest_possible_next_result_dist = sorted_edge_distances[0]
     
      if DEBUG:
        logging.debug(('GeoModel Proximity Query: '
                       'Next result at least %f meters away') %
                      (closest_possible_next_result_dist,))
     
      if max_distance and closest_possible_next_result_dist > max_distance:
        if DEBUG:
          logging.debug(('GeoModel Proximity Query: '
                         'Done! Next result at least %f meters away, '
                         'max disance is %f meters') %
                        (closest_possible_next_result_dist, max_distance))
        break
     
      if len(results) >= max_results:
        current_farthest_returnable_result_dist = \
            geomath.distance(center, results[max_results - 1][0].location)
        if (closest_possible_next_result_dist >=
            current_farthest_returnable_result_dist):
          if DEBUG:
            logging.debug(('GeoModel Proximity Query: '
                           'Done! Next result at least %f meters away, '
                           'current farthest is %f meters away') %
                          (closest_possible_next_result_dist,
                           current_farthest_returnable_result_dist))
          break
       
        if DEBUG:
          logging.debug(('GeoModel Proximity Query: '
                         'Next result at least %f meters away, '
                         'current farthest is %f meters away') %
                        (closest_possible_next_result_dist,
                         current_farthest_returnable_result_dist))

    if DEBUG:
      logging.debug(('GeoModel Proximity Query: '
                     'Looked in %d geocells') %
                    (len(searched_cells),))

    return [entity for (entity, dist) in results[:max_results]
            if not max_distance or dist < max_distance]


