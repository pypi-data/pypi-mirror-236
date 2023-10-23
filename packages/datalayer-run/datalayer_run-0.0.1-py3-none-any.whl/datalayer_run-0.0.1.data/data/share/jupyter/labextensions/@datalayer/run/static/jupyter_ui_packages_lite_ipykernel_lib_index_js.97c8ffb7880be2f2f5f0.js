"use strict";
(self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || []).push([["jupyter_ui_packages_lite_ipykernel_lib_index_js"],{

/***/ "../../jupyter/ui/packages/lite/ipykernel/lib/_pypi.js":
/*!*************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/ipykernel/lib/_pypi.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PIPLITE_WHEEL": () => (/* binding */ PIPLITE_WHEEL)
/* harmony export */ });
// export * as allJSONUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/all.json';
// export * as ipykernelWheelUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/ipykernel-6.9.2-py3-none-any.whl';
// export * as pipliteWheelUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/piplite-0.1.0b11-py3-none-any.whl';
// export * as pyoliteWheelUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/pyolite-0.1.0b11-py3-none-any.whl';
// export * as widgetsnbextensionWheelUrl from '!!file-loader?name=pypi/[name].[ext]&context=.!../pypi/widgetsnbextension-3.6.0-py3-none-any.whl';
const PIPLITE_WHEEL = 'piplite-0.1.0b11-py3-none-any.whl';


/***/ }),

/***/ "../../jupyter/ui/packages/lite/ipykernel/lib/index.js":
/*!*************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/ipykernel/lib/index.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PIPLITE_WHEEL": () => (/* reexport safe */ _pypi__WEBPACK_IMPORTED_MODULE_0__.PIPLITE_WHEEL),
/* harmony export */   "PyoliteKernel": () => (/* reexport safe */ _kernel__WEBPACK_IMPORTED_MODULE_1__.PyoliteKernel),
/* harmony export */   "PyoliteRemoteKernel": () => (/* reexport safe */ _worker__WEBPACK_IMPORTED_MODULE_2__.PyoliteRemoteKernel)
/* harmony export */ });
/* harmony import */ var _pypi__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./_pypi */ "../../jupyter/ui/packages/lite/ipykernel/lib/_pypi.js");
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./kernel */ "../../jupyter/ui/packages/lite/ipykernel/lib/kernel.js");
/* harmony import */ var _worker__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./worker */ "../../jupyter/ui/packages/lite/ipykernel/lib/worker.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/***/ }),

/***/ "../../jupyter/ui/packages/lite/ipykernel/lib/kernel.js":
/*!**************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/ipykernel/lib/kernel.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PyoliteKernel": () => (/* binding */ PyoliteKernel)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @datalayer/jupyterlite-kernel */ "../../jupyter/ui/packages/lite/kernel/lib/kernel.js");
/* harmony import */ var comlink__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! comlink */ "../../../node_modules/comlink/dist/esm/comlink.mjs");
/* harmony import */ var _pypi__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./_pypi */ "../../jupyter/ui/packages/lite/ipykernel/lib/_pypi.js");





/**
 * A kernel that executes Python code with Pyodide.
 */
class PyoliteKernel extends _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_2__.BaseKernel {
    /**
     * Instantiate a new PyodideKernel
     *
     * @param options The instantiation options for a new PyodideKernel
     */
    constructor(options) {
        super(options);
        this._worker = this.initWorker(options);
        this._worker.onmessage = (e) => this._processWorkerMessage(e.data);
        this._remoteKernel = this.initRemote(options);
        this._ready.resolve();
    }
    /**
     * Load the worker.
     *
     * ### Note
     *
     * Subclasses must implement this typographically almost _exactly_ for
     * webpack to find it.
     */
    initWorker(options) {
        return new Worker(new URL(/* worker import */ __webpack_require__.p + __webpack_require__.u("jupyter_ui_packages_lite_ipykernel_lib_comlink_worker_js"), __webpack_require__.b), {
            type: undefined,
        });
    }
    initRemote(options) {
        const remote = (0,comlink__WEBPACK_IMPORTED_MODULE_3__.wrap)(this._worker);
        const remoteOptions = this.initRemoteOptions(options);
        remote.initialize(remoteOptions);
        return remote;
    }
    initRemoteOptions(options) {
        const { pyodideUrl } = options;
        const indexUrl = pyodideUrl.slice(0, pyodideUrl.lastIndexOf('/') + 1);
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getBaseUrl();
        //    const pypi = URLExt.join(baseUrl, 'build/pypi');
        const pypi = "https://datalayer-assets.s3.us-west-2.amazonaws.com/pypi";
        const pipliteUrls = [...(options.pipliteUrls || []), _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(pypi, 'all.json')];
        const pipliteWheelUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(pypi, _pypi__WEBPACK_IMPORTED_MODULE_4__.PIPLITE_WHEEL);
        const disablePyPIFallback = !!options.disablePyPIFallback;
        return {
            baseUrl,
            pyodideUrl,
            indexUrl,
            pipliteWheelUrl,
            pipliteUrls,
            disablePyPIFallback,
            location: this.location,
            mountDrive: options.mountDrive,
        };
    }
    /**
     * Dispose the kernel.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._worker.terminate();
        this._worker = null;
        super.dispose();
    }
    /**
     * A promise that is fulfilled when the kernel is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Process a message coming from the pyodide web worker.
     *
     * @param msg The worker message to process.
     */
    _processWorkerMessage(msg) {
        if (!msg.type) {
            return;
        }
        switch (msg.type) {
            case 'stream': {
                const bundle = msg.bundle ?? { name: 'stdout', text: '' };
                this.stream(bundle, msg.parentHeader);
                break;
            }
            case 'input_request': {
                const bundle = msg.content ?? { prompt: '', password: false };
                this.inputRequest(bundle, msg.parentHeader);
                break;
            }
            case 'display_data': {
                const bundle = msg.bundle ?? { data: {}, metadata: {}, transient: {} };
                this.displayData(bundle, msg.parentHeader);
                break;
            }
            case 'update_display_data': {
                const bundle = msg.bundle ?? { data: {}, metadata: {}, transient: {} };
                this.updateDisplayData(bundle, msg.parentHeader);
                break;
            }
            case 'clear_output': {
                const bundle = msg.bundle ?? { wait: false };
                this.clearOutput(bundle, msg.parentHeader);
                break;
            }
            case 'execute_result': {
                const bundle = msg.bundle ?? { execution_count: 0, data: {}, metadata: {} };
                this.publishExecuteResult(bundle, msg.parentHeader);
                break;
            }
            case 'execute_error': {
                const bundle = msg.bundle ?? { ename: '', evalue: '', traceback: [] };
                this.publishExecuteError(bundle, msg.parentHeader);
                break;
            }
            case 'comm_msg':
            case 'comm_open':
            case 'comm_close': {
                this.handleComm(msg.type, msg.content, msg.metadata, msg.buffers, msg.parentHeader);
                break;
            }
        }
    }
    /**
     * Handle a kernel_info_request message
     */
    async kernelInfoRequest() {
        const content = {
            implementation: 'pyodide',
            implementation_version: '0.1.0',
            language_info: {
                codemirror_mode: {
                    name: 'python',
                    version: 3,
                },
                file_extension: '.py',
                mimetype: 'text/x-python',
                name: 'python',
                nbconvert_exporter: 'python',
                pygments_lexer: 'ipython3',
                version: '3.8',
            },
            protocol_version: '5.3',
            status: 'ok',
            banner: 'Pyolite: A WebAssembly-powered Python kernel backed by Pyodide',
            help_links: [
                {
                    text: 'Python (WASM) Kernel',
                    url: 'https://pyodide.org',
                },
            ],
        };
        return content;
    }
    /**
     * Handle an `execute_request` message
     *
     * @param msg The parent message.
     */
    async executeRequest(content) {
        const result = await this._remoteKernel.execute(content, this.parent);
        result.execution_count = this.executionCount;
        return result;
    }
    /**
     * Handle an complete_request message
     *
     * @param msg The parent message.
     */
    async completeRequest(content) {
        return await this._remoteKernel.complete(content, this.parent);
    }
    /**
     * Handle an `inspect_request` message.
     *
     * @param content - The content of the request.
     *
     * @returns A promise that resolves with the response message.
     */
    async inspectRequest(content) {
        return await this._remoteKernel.inspect(content, this.parent);
    }
    /**
     * Handle an `is_complete_request` message.
     *
     * @param content - The content of the request.
     *
     * @returns A promise that resolves with the response message.
     */
    async isCompleteRequest(content) {
        return await this._remoteKernel.isComplete(content, this.parent);
    }
    /**
     * Handle a `comm_info_request` message.
     *
     * @param content - The content of the request.
     *
     * @returns A promise that resolves with the response message.
     */
    async commInfoRequest(content) {
        return await this._remoteKernel.commInfo(content, this.parent);
    }
    /**
     * Send an `comm_open` message.
     *
     * @param msg - The comm_open message.
     */
    async commOpen(msg) {
        return await this._remoteKernel.commOpen(msg, this.parent);
    }
    /**
     * Send an `comm_msg` message.
     *
     * @param msg - The comm_msg message.
     */
    async commMsg(msg) {
        return await this._remoteKernel.commMsg(msg, this.parent);
    }
    /**
     * Send an `comm_close` message.
     *
     * @param close - The comm_close message.
     */
    async commClose(msg) {
        return await this._remoteKernel.commClose(msg, this.parent);
    }
    /**
     * Send an `input_reply` message.
     *
     * @param content - The content of the reply.
     */
    async inputReply(content) {
        return await this._remoteKernel.inputReply(content, this.parent);
    }
    _worker;
    _remoteKernel;
    _ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
}


/***/ }),

/***/ "../../jupyter/ui/packages/lite/kernel/lib/kernel.js":
/*!***********************************************************!*\
  !*** ../../jupyter/ui/packages/lite/kernel/lib/kernel.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BaseKernel": () => (/* binding */ BaseKernel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);


/**
 * A base kernel class handling basic kernel messaging.
 */
class BaseKernel {
    /**
     * Construct a new BaseKernel.
     *
     * @param options The instantiation options for a BaseKernel.
     */
    constructor(options) {
        const { id, name, location, sendMessage } = options;
        this._id = id;
        this._name = name;
        this._location = location;
        this._sendMessage = sendMessage;
    }
    /**
     * A promise that is fulfilled when the kernel is ready.
     */
    get ready() {
        return Promise.resolve();
    }
    /**
     * Return whether the kernel is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A signal emitted when the kernel is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Get the kernel id
     */
    get id() {
        return this._id;
    }
    /**
     * Get the name of the kernel
     */
    get name() {
        return this._name;
    }
    /**
     * The location in the virtual filesystem from which the kernel was started.
     */
    get location() {
        return this._location;
    }
    /**
     * The current execution count
     */
    get executionCount() {
        return this._executionCount;
    }
    /**
     * Get the last parent header
     */
    get parentHeader() {
        return this._parentHeader;
    }
    /**
     * Get the last parent message (mimic ipykernel's get_parent)
     */
    get parent() {
        return this._parent;
    }
    /**
     * Dispose the kernel.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposed.emit(void 0);
    }
    /**
     * Handle an incoming message from the client.
     *
     * @param msg The message to handle
     */
    async handleMessage(msg) {
        this._busy(msg);
        this._parent = msg;
        const msgType = msg.header.msg_type;
        switch (msgType) {
            case 'kernel_info_request':
                await this._kernelInfo(msg);
                break;
            case 'execute_request':
                await this._execute(msg);
                break;
            case 'input_reply':
                this.inputReply(msg.content);
                break;
            case 'inspect_request':
                await this._inspect(msg);
                break;
            case 'is_complete_request':
                await this._isCompleteRequest(msg);
                break;
            case 'complete_request':
                await this._complete(msg);
                break;
            case 'history_request':
                await this._historyRequest(msg);
                break;
            case 'comm_open':
                await this.commOpen(msg);
                break;
            case 'comm_msg':
                await this.commMsg(msg);
                break;
            case 'comm_close':
                await this.commClose(msg);
                break;
            default:
                break;
        }
        this._idle(msg);
    }
    /**
     * Stream an event from the kernel
     *
     * @param parentHeader The parent header.
     * @param content The stream content.
     */
    stream(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'stream',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `display_data` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The display_data content.
     */
    displayData(content, parentHeader = undefined) {
        // Make sure metadata is always set
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        content.metadata = content.metadata ?? {};
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'display_data',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `input_request` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The input_request content.
     */
    inputRequest(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'stdin',
            msgType: 'input_request',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send an `execute_result` message.
     *
     * @param parentHeader The parent header.
     * @param content The execute result content.
     */
    publishExecuteResult(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'execute_result',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send an `error` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The error content.
     */
    publishExecuteError(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'error',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `update_display_data` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The update_display_data content.
     */
    updateDisplayData(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'update_display_data',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `clear_output` message to the client.
     *
     * @param parentHeader The parent header.
     * @param content The clear_output content.
     */
    clearOutput(content, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: 'clear_output',
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Send a `comm` message to the client.
     *
     * @param .
     */
    handleComm(type, content, metadata, buffers, parentHeader = undefined) {
        const parentHeaderValue = typeof parentHeader !== 'undefined' ? parentHeader : this._parentHeader;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            channel: 'iopub',
            msgType: type,
            // TODO: better handle this
            session: parentHeaderValue?.session ?? '',
            parentHeader: parentHeaderValue,
            content,
            metadata,
            buffers,
        });
        this._sendMessage(message);
    }
    /**
     * Send an 'idle' status message.
     *
     * @param parent The parent message
     */
    _idle(parent) {
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'status',
            session: parent.header.session,
            parentHeader: parent.header,
            channel: 'iopub',
            content: {
                execution_state: 'idle',
            },
        });
        this._sendMessage(message);
    }
    /**
     * Send a 'busy' status message.
     *
     * @param parent The parent message.
     */
    _busy(parent) {
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'status',
            session: parent.header.session,
            parentHeader: parent.header,
            channel: 'iopub',
            content: {
                execution_state: 'busy',
            },
        });
        this._sendMessage(message);
    }
    /**
     * Handle a kernel_info_request message
     *
     * @param parent The parent message.
     */
    async _kernelInfo(parent) {
        const content = await this.kernelInfoRequest();
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'kernel_info_reply',
            channel: 'shell',
            session: parent.header.session,
            parentHeader: parent.header,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Handle a `history_request` message
     *
     * @param msg The parent message.
     */
    async _historyRequest(msg) {
        const historyMsg = msg;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'history_reply',
            channel: 'shell',
            parentHeader: historyMsg.header,
            session: msg.header.session,
            content: {
                status: 'ok',
                history: this._history,
            },
        });
        this._sendMessage(message);
    }
    /**
     * Send an `execute_input` message.
     *
     * @param msg The parent message.
     */
    _executeInput(msg) {
        const parent = msg;
        const code = parent.content.code;
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'execute_input',
            parentHeader: parent.header,
            channel: 'iopub',
            session: msg.header.session,
            content: {
                code,
                execution_count: this._executionCount,
            },
        });
        this._sendMessage(message);
    }
    /**
     * Handle an execute_request message.
     *
     * @param msg The parent message.
     */
    async _execute(msg) {
        const executeMsg = msg;
        const content = executeMsg.content;
        if (content.store_history) {
            this._executionCount++;
        }
        // TODO: handle differently
        this._parentHeader = executeMsg.header;
        this._executeInput(executeMsg);
        if (content.store_history) {
            this._history.push([0, 0, content.code]);
        }
        const reply = await this.executeRequest(executeMsg.content);
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'execute_reply',
            channel: 'shell',
            parentHeader: executeMsg.header,
            session: msg.header.session,
            content: reply,
        });
        this._sendMessage(message);
    }
    /**
     * Handle an complete_request message
     *
     * @param msg The parent message.
     */
    async _complete(msg) {
        const completeMsg = msg;
        const content = await this.completeRequest(completeMsg.content);
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'complete_reply',
            parentHeader: completeMsg.header,
            channel: 'shell',
            session: msg.header.session,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Handle an inspect_request message
     *
     * @param msg The parent message.
     */
    async _inspect(msg) {
        const inspectMsg = msg;
        const content = await this.inspectRequest(inspectMsg.content);
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'inspect_reply',
            parentHeader: inspectMsg.header,
            channel: 'shell',
            session: msg.header.session,
            content,
        });
        this._sendMessage(message);
    }
    /**
     * Handle an is_complete_request message
     *
     * @param msg The parent message.
     */
    async _isCompleteRequest(msg) {
        const isCompleteMsg = msg;
        const content = await this.isCompleteRequest(isCompleteMsg.content);
        const message = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.KernelMessage.createMessage({
            msgType: 'is_complete_reply',
            parentHeader: isCompleteMsg.header,
            channel: 'shell',
            session: msg.header.session,
            content,
        });
        this._sendMessage(message);
    }
    _id;
    _name;
    _location;
    _history = [];
    _executionCount = 0;
    _isDisposed = false;
    _disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
    _sendMessage;
    _parentHeader = undefined;
    _parent = undefined;
}


/***/ })

}]);
//# sourceMappingURL=jupyter_ui_packages_lite_ipykernel_lib_index_js.97c8ffb7880be2f2f5f0.js.map