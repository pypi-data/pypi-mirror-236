(self["webpackChunkknic_jupyter"] = self["webpackChunkknic_jupyter"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var dexie__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! dexie */ "webpack/sharing/consume/default/dexie/dexie");
/* harmony import */ var dexie__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(dexie__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! axios */ "webpack/sharing/consume/default/axios/axios");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_3__);
/* provided dependency */ var process = __webpack_require__(/*! process/browser */ "./node_modules/process/browser.js");




/**
 * Supported Jupyter Lab events in knic-jupyter
 */
const JUPYTER_LOADED_EVENT = 'JUPYTER_LOADED';
const NOTEBOOK_OPENED_EVENT = 'NOTEBOOK_OPENED';
const NOTEBOOK_LOADED_EVENT = 'NOTEBOOK_LOADED';
const CELL_SELECTED_EVENT = 'CELL_SELECTED';
const NOTEBOOK_MODIFIED_EVENT = 'NOTEBOOK_MODIFIED';
const CELL_EXECUTION_BEGIN_EVENT = 'CELL_EXECUTION_BEGIN';
const CELL_EXECUTED_END_EVENT = 'CELL_EXECUTION_END';
const CELL_MODIFIED_EVENT = 'CELL_MODIFIED';
/**
 * timeoutID for our cell modified event
 */
let timeoutID;
/**
 * Initialization data for knic-jupyter
 */
const USE_DEXIE = new Boolean(process.env.USE_DEXIE) || false;
let db;
const USER = new URLSearchParams(window.location.search).get('userid');
const SESSION = new URLSearchParams(window.location.search).get('sessionid');
const SERVER_ENDPOINT = `http://localhost:5642/knic/user/${USER}/event`;
let ENUMERATION = 0;
let NOTEBOOK_NAME = '';
let NOTEBOOK_SESSION = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
let ORIGINAL_CELL_DATA = [];
let notebookJustOpened = false;
const plugin = {
    id: 'knic-jupyter:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebookTracker) => {
        if (USE_DEXIE) {
            db = setupDB();
        }
        // Log jupyter loaded event
        onJupyterLoaded();
        notebookTracker.widgetAdded.connect(onWidgetAdded, undefined);
        notebookTracker.activeCellChanged.connect(logActiveCell, undefined);
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.connect(onCellExecutionEnded, undefined);
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executionScheduled.connect(onCellExecutionBegin, undefined);
    }
};
let timeout = undefined;
function setupDB() {
    db = new dexie__WEBPACK_IMPORTED_MODULE_2__.Dexie('database');
    db.version(1).stores({
        logs: '++id, eventName, data'
    });
    return db;
}
function toCellData(cellModel) {
    return {
        cellId: cellModel.id,
        type: cellModel.type,
        metadata: cellModel.metadata,
        value: cellModel.value.text
    };
}
function isCellModified(cellDataExecuted) {
    if (ORIGINAL_CELL_DATA.some(e => e.value.trim() === cellDataExecuted.value.trim())) {
        return false;
    }
    else {
        return true;
    }
}
async function onCellExecutionBegin(emitter, args) {
    if ((args === null || args === void 0 ? void 0 : args.cell.model) && args.cell.model.type === 'code') {
        const model = args.cell.model.toJSON();
        const event = {
            eventData: {
                cell: toCellData(args.cell.model),
                notebookName: NOTEBOOK_NAME,
                location: window.location.toString(),
                executionCount: model.execution_count
            },
            enumeration: ENUMERATION++,
            notebookSession: NOTEBOOK_SESSION,
            eventName: CELL_EXECUTION_BEGIN_EVENT,
            user: USER,
            session: SESSION,
            timestamp: new Date().toISOString()
        };
        if (USE_DEXIE) {
            await db.table('logs').add({
                eventName: CELL_EXECUTION_BEGIN_EVENT,
                data: JSON.stringify(event, null, 2)
            });
        }
        axios__WEBPACK_IMPORTED_MODULE_3___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
            headers: { 'Content-Type': 'application/json' }
        });
    }
}
async function onCellExecutionEnded(emitter, args) {
    if ((args === null || args === void 0 ? void 0 : args.cell.model) && args.cell.model.type === 'code') {
        const model = args.cell.model.toJSON();
        const errors = model.outputs
            .map((element) => {
            if (element.output_type === 'error') {
                const error = element;
                return {
                    errorName: error.ename,
                    errorText: error.evalue,
                    stackTrace: error.traceback
                };
            }
            return { errorName: '', errorText: '', stackTrace: [] };
        })
            .filter(value => {
            return value.errorName !== '';
        });
        const outputs = model.outputs
            .map((element) => {
            if (element.output_type === 'stream') {
                return element.text;
            }
            else {
                return [];
            }
        })
            .filter(value => {
            return value.length > 0;
        });
        const event = {
            eventData: {
                cell: toCellData(args.cell.model),
                notebookName: NOTEBOOK_NAME,
                location: window.location.toString(),
                output: outputs,
                executionCount: model.execution_count,
                errors: errors
            },
            enumeration: ENUMERATION++,
            notebookSession: NOTEBOOK_SESSION,
            eventName: CELL_EXECUTED_END_EVENT,
            session: SESSION,
            user: USER,
            timestamp: new Date().toISOString()
        };
        axios__WEBPACK_IMPORTED_MODULE_3___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
            headers: { 'Content-Type': 'application/json' }
        });
    }
}
async function onWidgetAdded(emitter, args) {
    notebookJustOpened = true;
    args.content.modelContentChanged.connect(onModelContentChanged);
    ENUMERATION = 0;
    NOTEBOOK_SESSION = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
    NOTEBOOK_NAME = args.context.path;
    const event = {
        eventData: {
            notebookName: NOTEBOOK_NAME,
            location: window.location.toString()
        },
        user: USER,
        session: SESSION,
        enumeration: ENUMERATION++,
        notebookSession: NOTEBOOK_SESSION,
        timestamp: new Date().toISOString(),
        eventName: NOTEBOOK_OPENED_EVENT
    };
    if (USE_DEXIE) {
        await db.table('logs').add({
            eventName: NOTEBOOK_OPENED_EVENT,
            data: JSON.stringify(event, null, 2)
        });
    }
    axios__WEBPACK_IMPORTED_MODULE_3___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
        headers: { 'Content-Type': 'application/json' }
    });
}
async function onJupyterLoaded() {
    ENUMERATION = 0;
    NOTEBOOK_SESSION = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
    const event = {
        eventData: {
            location: window.location.toString()
        },
        user: USER,
        session: SESSION,
        enumeration: ENUMERATION++,
        notebookSession: NOTEBOOK_SESSION,
        timestamp: new Date().toISOString(),
        eventName: JUPYTER_LOADED_EVENT
    };
    if (USE_DEXIE) {
        await db.table('logs').add({
            eventName: JUPYTER_LOADED_EVENT,
            data: JSON.stringify(event, null, 2)
        });
    }
    axios__WEBPACK_IMPORTED_MODULE_3___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
        headers: { 'Content-Type': 'application/json' }
    });
}
async function onModelContentChanged(emitter) {
    if (notebookJustOpened) {
        notebookJustOpened = false;
        setTimeout(async () => {
            var _a;
            const cells = [];
            if ((_a = emitter.model) === null || _a === void 0 ? void 0 : _a.cells) {
                for (let index = 0; index < emitter.model.cells.length; index++) {
                    const cellModel = emitter.model.cells.get(index);
                    cells.push(toCellData(cellModel));
                    ORIGINAL_CELL_DATA.push(toCellData(cellModel));
                }
            }
            const event = {
                eventData: {
                    notebookName: NOTEBOOK_NAME,
                    location: window.location.toString(),
                    cells: cells
                },
                enumeration: ENUMERATION++,
                notebookSession: NOTEBOOK_SESSION,
                eventName: NOTEBOOK_LOADED_EVENT,
                user: USER,
                session: SESSION,
                timestamp: new Date().toISOString()
            };
            if (USE_DEXIE)
                await db.table('logs').add({
                    eventName: NOTEBOOK_LOADED_EVENT,
                    data: JSON.stringify(event, null, 2)
                });
            axios__WEBPACK_IMPORTED_MODULE_3___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
                headers: { 'Content-Type': 'application/json' }
            });
        }, 1000);
    }
    else {
        if (timeout) {
            clearTimeout(timeout);
        }
        timeout = setTimeout(async () => {
            var _a;
            const cells = [];
            if ((_a = emitter.model) === null || _a === void 0 ? void 0 : _a.cells) {
                for (let index = 0; index < emitter.model.cells.length; index++) {
                    const cellModel = emitter.model.cells.get(index);
                    cells.push(toCellData(cellModel));
                    ORIGINAL_CELL_DATA.push(toCellData(cellModel));
                }
            }
            const event = {
                eventData: {
                    notebookName: NOTEBOOK_NAME,
                    location: window.location.toString(),
                    cells: cells
                },
                enumeration: ENUMERATION++,
                notebookSession: NOTEBOOK_SESSION,
                eventName: NOTEBOOK_MODIFIED_EVENT,
                user: USER,
                session: SESSION,
                timestamp: new Date().toISOString()
            };
            if (USE_DEXIE) {
                await db.table('logs').add({
                    eventName: NOTEBOOK_MODIFIED_EVENT,
                    data: JSON.stringify(event, null, 2)
                });
            }
            axios__WEBPACK_IMPORTED_MODULE_3___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
                headers: { 'Content-Type': 'application/json' }
            });
        }, 5000);
    }
}
async function logActiveCell(emitter, args) {
    if (args === null || args === void 0 ? void 0 : args.model) {
        const event = {
            eventData: {
                cell: toCellData(args === null || args === void 0 ? void 0 : args.model),
                notebookName: NOTEBOOK_NAME,
                location: window.location.toString()
            },
            enumeration: ENUMERATION++,
            notebookSession: NOTEBOOK_SESSION,
            eventName: CELL_SELECTED_EVENT,
            user: USER,
            session: SESSION,
            timestamp: new Date().toISOString()
        };
        if (USE_DEXIE) {
            await db.table('logs').add({
                eventName: CELL_SELECTED_EVENT,
                data: JSON.stringify(event, null, 2)
            });
        }
        axios__WEBPACK_IMPORTED_MODULE_3___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
            headers: { 'Content-Type': 'application/json' }
        });
    }
    // connect onContentChanged listener to the cell model
    args === null || args === void 0 ? void 0 : args.model.contentChanged.connect(logDisplayChange);
}
async function logDisplayChange(args) {
    if (args) {
        const cellData = toCellData(args);
        if (isCellModified(cellData)) {
            clearTimeout(timeoutID);
            timeoutID = setTimeout(() => {
                const event = {
                    eventData: {
                        cell: cellData,
                        notebookName: NOTEBOOK_NAME,
                        location: window.location.toString(),
                        changeEvents: [cellData],
                    },
                    enumeration: ENUMERATION++,
                    notebookSession: NOTEBOOK_SESSION,
                    eventName: CELL_MODIFIED_EVENT,
                    user: USER,
                    session: SESSION,
                    timestamp: new Date().toISOString()
                };
                axios__WEBPACK_IMPORTED_MODULE_3___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
                    headers: { 'Content-Type': 'application/json' }
                });
            }, 1000); // 1 second delay
        }
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./node_modules/process/browser.js":
/*!*****************************************!*\
  !*** ./node_modules/process/browser.js ***!
  \*****************************************/
/***/ ((module) => {

// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;

function defaultSetTimout() {
    throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout () {
    throw new Error('clearTimeout has not been defined');
}
(function () {
    try {
        if (typeof setTimeout === 'function') {
            cachedSetTimeout = setTimeout;
        } else {
            cachedSetTimeout = defaultSetTimout;
        }
    } catch (e) {
        cachedSetTimeout = defaultSetTimout;
    }
    try {
        if (typeof clearTimeout === 'function') {
            cachedClearTimeout = clearTimeout;
        } else {
            cachedClearTimeout = defaultClearTimeout;
        }
    } catch (e) {
        cachedClearTimeout = defaultClearTimeout;
    }
} ())
function runTimeout(fun) {
    if (cachedSetTimeout === setTimeout) {
        //normal enviroments in sane situations
        return setTimeout(fun, 0);
    }
    // if setTimeout wasn't available but was latter defined
    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
        cachedSetTimeout = setTimeout;
        return setTimeout(fun, 0);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedSetTimeout(fun, 0);
    } catch(e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
            return cachedSetTimeout.call(null, fun, 0);
        } catch(e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
            return cachedSetTimeout.call(this, fun, 0);
        }
    }


}
function runClearTimeout(marker) {
    if (cachedClearTimeout === clearTimeout) {
        //normal enviroments in sane situations
        return clearTimeout(marker);
    }
    // if clearTimeout wasn't available but was latter defined
    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
        cachedClearTimeout = clearTimeout;
        return clearTimeout(marker);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedClearTimeout(marker);
    } catch (e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
            return cachedClearTimeout.call(null, marker);
        } catch (e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
            return cachedClearTimeout.call(this, marker);
        }
    }



}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    if (!draining || !currentQueue) {
        return;
    }
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = runTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    runClearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        runTimeout(drainQueue);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop() {}

process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;

process.listeners = function (name) { return [] }

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };


/***/ })

}]);
//# sourceMappingURL=lib_index_js.613217a0676eacec00e4.js.map