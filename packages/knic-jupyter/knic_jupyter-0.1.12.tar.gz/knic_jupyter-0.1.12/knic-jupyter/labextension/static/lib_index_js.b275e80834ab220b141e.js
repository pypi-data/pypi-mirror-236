"use strict";
(self["webpackChunkknic_jupyter"] = self["webpackChunkknic_jupyter"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! axios */ "webpack/sharing/consume/default/axios/axios");
/* harmony import */ var axios__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(axios__WEBPACK_IMPORTED_MODULE_2__);



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
        // Log jupyter loaded event
        onJupyterLoaded();
        notebookTracker.widgetAdded.connect(onWidgetAdded, undefined);
        notebookTracker.activeCellChanged.connect(logActiveCell, undefined);
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.connect(onCellExecutionEnded, undefined);
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executionScheduled.connect(onCellExecutionBegin, undefined);
    }
};
let timeout = undefined;
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
        axios__WEBPACK_IMPORTED_MODULE_2___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
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
        axios__WEBPACK_IMPORTED_MODULE_2___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
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
    axios__WEBPACK_IMPORTED_MODULE_2___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
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
    axios__WEBPACK_IMPORTED_MODULE_2___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
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
            axios__WEBPACK_IMPORTED_MODULE_2___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
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
            axios__WEBPACK_IMPORTED_MODULE_2___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
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
        axios__WEBPACK_IMPORTED_MODULE_2___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
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
                axios__WEBPACK_IMPORTED_MODULE_2___default().post(SERVER_ENDPOINT, encodeURI(JSON.stringify(event)), {
                    headers: { 'Content-Type': 'application/json' }
                });
            }, 1000); // 1 second delay
        }
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b275e80834ab220b141e.js.map