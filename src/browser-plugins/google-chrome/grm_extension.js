/**
 * BACKGROUND PROCESS (Notifier)
 */

var GRMNotifify = {};
window.GRMNotifify = GRMNotifify;

/**
 * Default settings
 */
GRMNotifify.defaultSettings = {};
GRMNotifify.defaultSettings.refreshtime = 2;
GRMNotifify.defaultSettings.apihost = 'http://localhost:8080';

/**
 * Current running settings.
 */
GRMNotifify.settings = {};

// Some system state
GRMNotifify.unreadCount = 0;
GRMNotifify.notifications = [];
GRMNotifify.lastEncounteredObjectId = 0;
GRMNotifify.lastSeenObjectId = localStorage.lastSeenObjectId;


/**
 * Update the current running settings to be the user given setting or the default.
 */
GRMNotifify.updateSettings = function() {
    GRMNotifify.settings.refreshtime = localStorage.refreshtime || GRMNotifify.defaultSettings.refreshtime;
    GRMNotifify.settings.apihost = localStorage.apihost || GRMNotifify.defaultSettings.apihost;
};

/**
 * Ids of items which have been notified.
 */
GRMNotifify.notifiedIds = [];

/**
 * Request the activity stream.
 * Relies on the user being authenticated on georemindme.com already.
 */
GRMNotifify.fetchActivity = function() {
    var xhr = new XMLHttpRequest();

    xhr.open("POST", GRMNotifify.settings.apihost + "/ajax/get/activity/");

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.responseText.indexOf('<!DOCTYPE html>') > -1) {
                // Not logged in apparently.
                //chrome.browserAction.setIcon({path: 'icon_notloggedin.png'});
                chrome.browserAction.setTitle({title: 'Error: Not logged in to georemindme.com'});
                // Die.
                return;
            }

            // If we're authenticated, reset to default settings.
            //chrome.browserAction.setIcon({path: 'icon.png'});
            chrome.browserAction.setTitle({title: 'GeoRemindMe! extension'});

            var response = _.parseFromAPI(JSON.parse(xhr.responseText));

            GRMNotifify.processActivityResponse(response);
        }
    };

    xhr.send();
};

/**
 * Process the activity stream data.
 * Update / notify with result.
 */
GRMNotifify.processActivityResponse = function(objects) {
    if (!objects[0]) { return; }

    var showNotifications = true;

    var unreadCount = 0;
    var startPos = 0;

    if (GRMNotifify.lastSeenObjectId) {
        for (var iter = objects.length - 1, item; item = objects[iter]; iter--) {
            if (item.id == GRMNotifify.lastSeenObjectId) {
                startPos = iter - 1;
                break;
            }
        }
    } else {
        startPos = objects.length - 1;
        showNotifications = false;
    }

    // For each activity...
    _(objects).chain().reverse().each(function (item) {
        // See if we've displayed a notification for this item yet.
        if (GRMNotifify.notifiedIds.indexOf(item.id) == -1) {

            // We found the targeted item by the activity, hooray!
            if (item.target) {

                var showItem = true;

                var notificationBody = '';
                var notificationBodyHtml; // will default to the body
                var notificationAction = item.project.name + ': [' + item.target.type + '] ' + item.target.name;
                var notificationURL = item.target.url();

                notificationBodyHtml = item.target.body_html || item.target.body || item.target.name;
                notificationBody = item.target.body || item.target.name;

                switch (item.target.target_type) {
                    case 'Conversation':
                        // Check if a conversation is a "simple" one (activity feed only).
                        // If so, don't show the conversation as a notification
                        if (item.target.simple === true) {
                            // We never show this, since, it's a useless item to an end user
                            showItem = false;
                            notificationAction = item.project.name + ' conversation';
                        } else {
                            notificationAction = item.project.name + ': [' + item.target.target.type + '] ' + item.target.target.name;
                        }
                        notificationURL = item.target.target.url();
                        break;
                    case 'Task':
                        notificationAction = item.project.name + ': [' + item.target.target.type + '] ' + item.target.target.name;
                        notificationURL = item.target.target.url();

                        // It appears this means a task was changed or commented on in some way
                        if (item.target.type == 'Comment') {
                            // If there's no body (a non text comment change, probably assignment or due date, etc).
                            if (!notificationBody) {
                                // This is shitty and we should try and tell the user what actually happened, if possible.
                                notificationBody = 'Updated Task...';
                            }
                        }
                        break;
                }

                if (showItem) {
                    unreadCount++;

                    GRMNotifify.notifications.push({
                        img: item.user.avatar_url,
                        type: notificationAction,
                        body: notificationBody,
                        bodyHtml: notificationBodyHtml || notificationBody,
                        url: GRMNotifify.settings.apihost + notificationURL
                    });

                    if (showNotifications) {
                        // Meh, let's scope this so I can just use notification for all
                        // of them and they can just quickly reference back to it.
                        // I hate closures. This is nasty.
                        (function() {
                            var notification = webkitNotifications.createNotification(
                                item.user.avatar_url,
                                notificationAction,
                                notificationBody
                            );

                            notification.show();

                            setTimeout(function() {
                                notification.cancel();
                            }, 10000);
                        })();
                    }
                }

                GRMNotifify.notifiedIds.unshift(item.id);
            }
        }
    });

    GRMNotifify.unreadCount += unreadCount;

    if (GRMNotifify.unreadCount) {
        chrome.browserAction.setBadgeText({text: "" + GRMNotifify.unreadCount});
    } else {
        chrome.browserAction.setBadgeText({text: ""});
    }

    // Store so that we can sync this to our last seen when button is pressed
    GRMNotifify.lastEncounteredObjectId = objects[0].id;

    // Wipe out any ids past the last 100.
    GRMNotifify.notifiedIds.splice(100);
};

GRMNotifify.getActionVerb = function(action) {
    switch (action) {
        case 'create': return 'New';
        case 'edit':   return 'Updated';
        default:       return action;
    }
};

/**
 * Handler for when the user clicks on the icon in the bar.
 */
GRMNotifify.handleButtonClicked = function() {
    chrome.browserAction.setBadgeText({"text": ""});
    localStorage.lastSeenObjectId = GRMNotifify.lastSeenObjectId = GRMNotifify.lastEncounteredObjectId;
    GRMNotifify.unreadCount = 0;
};

GRMNotifify.popupOpened = function() {
    GRMNotifify.handleButtonClicked();
};

GRMNotifify.refresh = function() {
    GRMNotifify.fetchActivity();

    window.setTimeout(GRMNotifify.refresh, 60000 * parseInt(GRMNotifify.settings.refreshtime, 10));
};

// Immediately initialize our settings
GRMNotifify.updateSettings();

chrome.browserAction.onClicked.addListener(GRMNotifify.handleButtonClicked);

// Start loading
GRMNotifify.refresh();
