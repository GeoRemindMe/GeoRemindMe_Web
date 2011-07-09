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

"""Defines utility functions used throughout the geocell/GeoModel library."""

__author__ = 'api.roman.public@gmail.com (Roman Nurik)'

import copy
import logging
import math

import asynctools

import geocell
import geomath
import geotypes


def merge_in_place(*lists, **kwargs):
  """Merges pre-sorted lists.
  
  Merges an arbitrary number of pre-sorted lists in-place, into the first
  list, possibly pruning out duplicates. Source lists must not have
  duplicates.

  Args:
    list1: The first, sorted list into which the other lists should be merged.
    list2: A subsequent, sorted list to merge into the first.
    ...
    listn:  "   "
    cmp_fn: An optional binary comparison function that compares objects across
        lists and determines the merged list's sort order.
    dup_fn: An optional binary comparison function that should return True if
        the given objects are equivalent and one of them can be pruned from the
        resulting merged list.

  Returns:
    list1, in-placed merged wit the other lists, or an empty list if no lists
    were specified.
  """
  cmp_fn = kwargs.get('cmp_fn') or cmp
  dup_fn = kwargs.get('dup_fn') or None

  if not lists:
    return []

  reverse_indices = [len(arr) for arr in lists]
  aggregate_reverse_index = sum(reverse_indices)

  while aggregate_reverse_index > 0:
    pull_arr_index = None
    pull_val = None

    for i in range(len(lists)):
      if reverse_indices[i] == 0:
        # Reached the end of this list.
        pass
      elif (pull_arr_index is not None and
            dup_fn and dup_fn(lists[i][-reverse_indices[i]], pull_val)):
        # Found a duplicate, advance the index of the list in which the
        # duplicate was found.
        reverse_indices[i] -= 1
        aggregate_reverse_index -= 1
      elif (pull_arr_index is None or
            cmp_fn(lists[i][-reverse_indices[i]], pull_val) < 0):
        # Found a lower value.
        pull_arr_index = i
        pull_val = lists[i][-reverse_indices[i]]

    if pull_arr_index != 0:
      # Add the lowest found value in place into the first array.
      lists[0].insert(len(lists[0]) - reverse_indices[0], pull_val)

    aggregate_reverse_index -= 1
    reverse_indices[pull_arr_index] -= 1

  return lists[0]


def max_box(cells):
  """Returns the rectangular region containing all of the given geocells.
  
  Args:
    cells: A list of adjacent geocells.
  
  Returns:
    A geotypes.Box representing the maximum bounds of the set of adjacent cells.
  """
  boxes = [geocell.compute_box(cell) for cell in cells]
  return geotypes.Box(max([box.north for box in boxes]),
                      max([box.east for box in boxes]),
                      min([box.south for box in boxes]),
                      min([box.west for box in boxes]))


def distance_sorted_edges(box, point):
  """Returns the edge directions of the box, sorted by distance from a point.
  
  Returns the edge directions (i.e. NORTH, SOUTH, etc.) of the box, sorted by
  distance from the given point, along with the actual distances from the point
  to these edges.

  Args:
    box: The geotypes.Box defining the rectangular region whose edge distances
        are requested.
    point: The point that should determine the edge sort order.

  Returns:
    A list of (direction, distance) tuples, where direction is the edge
    direction and distance is the distance from the point to that edge.
    Direction values will be NORTH, SOUTH, EAST, or WEST
  """
  # TODO(romannurik): Assert that lat,lon are actually inside the box.
  return zip(*sorted([
      (geocell.NORTH,
       geomath.distance(geotypes.Point(box.north, point.lon), point)),
      (geocell.SOUTH,
       geomath.distance(geotypes.Point(box.south, point.lon), point)),
      (geocell.WEST,
       geomath.distance(geotypes.Point(point.lat, box.west), point)),
      (geocell.EAST,
       geomath.distance(geotypes.Point(point.lat, box.east), point))],
      lambda x, y: cmp(x[1], y[1])))


def async_in_query_fetch(query, property_name, values, max_results=1000,
                         debug=False):
  """Fetches query results asynchronously, with an extra IN filter applied.
  
  Args:
    query: The base db.Query to query on.
    property_name: A str representing the property to filter on.
    values: A list of acceptable values for the property, to filter on.
    max_results: An optional int for the maximum number of results to return.
    debug: A boolean indicating whether or not to log debug info.
  
  Returns:
    The fetched entities.
  
  Raises:
    Any exceptions that google.appengine.ext.db.Query.fetch() can raise.
  """
  if not values:
    return []

  # Parallelize queries using asynctools.
  task_runner = asynctools.AsyncMultiTask()
  
  for value in values:
    task_runner.append(asynctools.QueryTask(
        copy.deepcopy(query).filter('%s =' % property_name, value),
        limit=max_results))
  
  task_runner.run()
  entities_by_value = [task.get_result() for task in task_runner]
  
  if debug:
    logging.debug(('GeoModel: '
                   'Fetch complete for %s = %s') %
                  (property_name, ','.join(values)))
  
  if query._Query__orderings:
    # Manual in-memory sort on the query's defined ordering.
    query_orderings = query._Query__orderings or []
    def _ordering_fn(ent1, ent2):
      for prop, direction in query_orderings:
        prop_cmp = cmp(getattr(ent1, prop), getattr(ent2, prop))
        if prop_cmp != 0:
          return prop_cmp if direction == 1 else -prop_cmp

      return -1  # Default ent1 < ent2.

    merge_in_place(cmp_fn=_ordering_fn,
                   dup_fn=lambda x, y: x.key() == y.key(),
                   *entities_by_value)
    return entities_by_value[0][:max_results]
  else:
    # Return max_results entities, proportionally by geocell, since there
    # is no ordering.
    total_results = sum(len(val_entities) for val_entities in entities_by_value)
    if not total_results:
      return []
    _numkeep = lambda arr: int(math.ceil(len(arr) * 1.0 / total_results))
    entities_by_value = [val_entities[:_numkeep(val_entities)]
                         for val_entities in entities_by_value]
    return reduce(lambda x, y: x + y, entities_by_value)
'''


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

"""Defines utility functions used throughout the geocell/GeoModel library."""

__author__ = 'api.roman.public@gmail.com (Roman Nurik)'

import copy
import logging
import math


import geocell
import geomath
import geotypes
from google.appengine.ext import db
from google.appengine.datastore import datastore_query


def merge_in_place(*lists, **kwargs):
  """Merges pre-sorted lists.
  
  Merges an arbitrary number of pre-sorted lists in-place, into the first
  list, possibly pruning out duplicates. Source lists must not have
  duplicates.

  Args:
    list1: The first, sorted list into which the other lists should be merged.
    list2: A subsequent, sorted list to merge into the first.
    ...
    listn:  "   "
    cmp_fn: An optional binary comparison function that compares objects across
        lists and determines the merged list's sort order.
    dup_fn: An optional binary comparison function that should return True if
        the given objects are equivalent and one of them can be pruned from the
        resulting merged list.

  Returns:
    list1, in-placed merged wit the other lists, or an empty list if no lists
    were specified.
  """
  cmp_fn = kwargs.get('cmp_fn') or cmp
  dup_fn = kwargs.get('dup_fn') or None

  if not lists:
    return []

  reverse_indices = [len(arr) for arr in lists]
  aggregate_reverse_index = sum(reverse_indices)

  while aggregate_reverse_index > 0:
    pull_arr_index = None
    pull_val = None

    for i in range(len(lists)):
      if reverse_indices[i] == 0:
        # Reached the end of this list.
        pass
      elif (pull_arr_index is not None and
            dup_fn and dup_fn(lists[i][-reverse_indices[i]], pull_val)):
        # Found a duplicate, advance the index of the list in which the
        # duplicate was found.
        reverse_indices[i] -= 1
        aggregate_reverse_index -= 1
      elif (pull_arr_index is None or
            cmp_fn(lists[i][-reverse_indices[i]], pull_val) < 0):
        # Found a lower value.
        pull_arr_index = i
        pull_val = lists[i][-reverse_indices[i]]

    if pull_arr_index != 0:
      # Add the lowest found value in place into the first array.
      lists[0].insert(len(lists[0]) - reverse_indices[0], pull_val)

    aggregate_reverse_index -= 1
    reverse_indices[pull_arr_index] -= 1

  return lists[0]


def max_box(cells):
  """Returns the rectangular region containing all of the given geocells.
  
  Args:
    cells: A list of adjacent geocells.
  
  Returns:
    A geotypes.Box representing the maximum bounds of the set of adjacent cells.
  """
  boxes = [geocell.compute_box(cell) for cell in cells]
  return geotypes.Box(max([box.north for box in boxes]),
                      max([box.east for box in boxes]),
                      min([box.south for box in boxes]),
                      min([box.west for box in boxes]))


def distance_sorted_edges(box, point):
  """Returns the edge directions of the box, sorted by distance from a point.
  
  Returns the edge directions (i.e. NORTH, SOUTH, etc.) of the box, sorted by
  distance from the given point, along with the actual distances from the point
  to these edges.

  Args:
    box: The geotypes.Box defining the rectangular region whose edge distances
        are requested.
    point: The point that should determine the edge sort order.

  Returns:
    A list of (direction, distance) tuples, where direction is the edge
    direction and distance is the distance from the point to that edge.
    Direction values will be NORTH, SOUTH, EAST, or WEST
  """
  # TODO(romannurik): Assert that lat,lon are actually inside the box.
  return zip(*sorted([
      (geocell.NORTH,
       geomath.distance(geotypes.Point(box.north, point.lon), point)),
      (geocell.SOUTH,
       geomath.distance(geotypes.Point(box.south, point.lon), point)),
      (geocell.WEST,
       geomath.distance(geotypes.Point(point.lat, box.west), point)),
      (geocell.EAST,
       geomath.distance(geotypes.Point(point.lat, box.east), point))],
      lambda x, y: cmp(x[1], y[1])))


def async_in_query_fetch(query, property_name, values, max_results=1000,
                         debug=False):
  """Fetches query results asynchronously, with an extra IN filter applied.
  
  Args:
    query: The base db.Query to query on.
    property_name: A str representing the property to filter on.
    values: A list of acceptable values for the property, to filter on.
    max_results: An optional int for the maximum number of results to return.
    debug: A boolean indicating whether or not to log debug info.
  
  Returns:
    The fetched entities.
  
  Raises:
    Any exceptions that google.appengine.ext.db.Query.fetch() can raise.
  """
  if not values:
    return []

  # Parallelize queries using asynctools.
  entities_by_value = []
  for value in values:
    entities_by_value.append(
        query.filter('location_geocells =', value).run(
                config=datastore_query.QueryOptions(limit=max_results)))
  print values
  print entities_by_value
  if debug:
    logging.debug(('GeoModel: '
                   'Fetch complete for %s = %s') % 
                  (property_name, ','.join(values)))
  
  if query._Query__orderings:
    # Manual in-memory sort on the query's defined ordering.
    query_orderings = query._Query__orderings or []
    def _ordering_fn(ent1, ent2):
      for prop, direction in query_orderings:
        prop_cmp = cmp(getattr(ent1, prop), getattr(ent2, prop))
        if prop_cmp != 0:
          return prop_cmp if direction == 1 else - prop_cmp

      return - 1  # Default ent1 < ent2.

    merge_in_place(cmp_fn=_ordering_fn,
                   dup_fn=lambda x, y: x.key() == y.key(),
                   *entities_by_value)
    return entities_by_value[0][:max_results]
  else:
    # Return max_results entities, proportionally by geocell, since there
    # is no ordering.
    results = []
    iters = [iter(val_entities) for val_entities in entities_by_value]
    iter_index = 0
    while len(results) < max_results and len(iters) > 0:
        iter_index = iter_index%len(iters)
        current_iter = iters[iter_index]
        try:
            results.append(current_iter.next())
            iter_index = iter_index + 1
        except StopIteration:
            del iters[iter_index]
    
    return results

'''