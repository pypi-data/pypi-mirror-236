"use strict";
(self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || []).push([["jupyter_ui_packages_lite_ipykernel_lib_worker_js"],{

/***/ "../../jupyter/ui/packages/lite/ipykernel/lib/worker.js":
/*!**************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/ipykernel/lib/worker.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PyoliteRemoteKernel": () => (/* binding */ PyoliteRemoteKernel)
/* harmony export */ });
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
class PyoliteRemoteKernel {
    constructor() {
        this._initialized = new Promise((resolve, reject) => {
            this._initializer = { resolve, reject };
        });
    }
    /**
     * Accept the URLs from the host
     **/
    async initialize(options) {
        this._options = options;
        if (options.location.includes(':')) {
            const parts = options.location.split(':');
            this._driveName = parts[0];
            this._localPath = parts[1];
        }
        else {
            this._driveName = '';
            this._localPath = options.location;
        }
        await this.initRuntime(options);
        await this.initPackageManager(options);
        await this.initKernel(options);
        await this.initGlobals(options);
        this._initializer?.resolve();
    }
    async initRuntime(options) {
        const { pyodideUrl, indexUrl } = options;
        if (pyodideUrl.endsWith('.mjs')) {
            const pyodideModule = await import(/* webpackIgnore: true */ pyodideUrl);
            this._pyodide = await pyodideModule.loadPyodide({ indexURL: indexUrl });
        }
        else {
            importScripts(pyodideUrl);
            this._pyodide = await self.loadPyodide({ indexURL: indexUrl });
        }
    }
    async initPackageManager(options) {
        if (!this._options) {
            throw new Error('Uninitialized');
        }
        const { pipliteWheelUrl, disablePyPIFallback, pipliteUrls } = this._options;
        // this is the only use of `loadPackage`, allow `piplite` to handle the rest
        await this._pyodide.loadPackage(['micropip']);
        // get piplite early enough to impact pyolite dependencies
        await this._pyodide.runPythonAsync(`
      import micropip
      await micropip.install('${pipliteWheelUrl}', keep_going=True)
      import piplite.piplite
      piplite.piplite._PIPLITE_DISABLE_PYPI = ${disablePyPIFallback ? 'True' : 'False'}
      piplite.piplite._PIPLITE_URLS = ${JSON.stringify(pipliteUrls)}
    `);
    }
    async initKernel(options) {
        // from this point forward, only use piplite
        await this._pyodide.runPythonAsync(`
      await piplite.install(['matplotlib', 'ipykernel'], keep_going=True);
      await piplite.install(['pyolite'], keep_going=True);
      await piplite.install(['ipython'], keep_going=True);
      import pyolite
    `);
        // cd to the kernel location
        if (options.mountDrive && this._localPath) {
            await this._pyodide.runPythonAsync(`
        import os;
        os.chdir("${this._localPath}");
      `);
        }
    }
    async initGlobals(options) {
        const { globals } = this._pyodide;
        this._kernel = globals.get('pyolite').kernel_instance.copy();
        this._stdout_stream = globals.get('pyolite').stdout_stream.copy();
        this._stderr_stream = globals.get('pyolite').stderr_stream.copy();
        this._interpreter = this._kernel.interpreter.copy();
        this._interpreter.send_comm = this.sendComm.bind(this);
    }
    /**
     * Recursively convert a Map to a JavaScript object
     * @param obj A Map, Array, or other  object to convert
     */
    mapToObject(obj) {
        const out = obj instanceof Array ? [] : {};
        obj.forEach((value, key) => {
            out[key] =
                value instanceof Map || value instanceof Array
                    ? this.mapToObject(value)
                    : value;
        });
        return out;
    }
    /**
     * Format the response from the Pyodide evaluation.
     *
     * @param res The result object from the Pyodide evaluation
     */
    formatResult(res) {
        if (!this._pyodide.isPyProxy(res)) {
            return res;
        }
        // TODO: this is a bit brittle
        const m = res.toJs();
        const results = this.mapToObject(m);
        return results;
    }
    /**
     * Makes sure pyodide is ready before continuing, and cache the parent message.
     */
    async setup(parent) {
        await this._initialized;
        this._kernel._parent_header = this._pyodide.toPy(parent);
    }
    /**
     * Execute code with the interpreter.
     *
     * @param content The incoming message with the code to execute.
     */
    async execute(content, parent) {
        await this.setup(parent);
        const publishExecutionResult = (prompt_count, data, metadata) => {
            const bundle = {
                execution_count: prompt_count,
                data: this.formatResult(data),
                metadata: this.formatResult(metadata),
            };
            postMessage({
                parentHeader: this.formatResult(this._kernel._parent_header)['header'],
                bundle,
                type: 'execute_result',
            });
        };
        const publishExecutionError = (ename, evalue, traceback) => {
            const bundle = {
                ename: ename,
                evalue: evalue,
                traceback: traceback,
            };
            postMessage({
                parentHeader: this.formatResult(this._kernel._parent_header)['header'],
                bundle,
                type: 'execute_error',
            });
        };
        const clearOutputCallback = (wait) => {
            const bundle = {
                wait: this.formatResult(wait),
            };
            postMessage({
                parentHeader: this.formatResult(this._kernel._parent_header)['header'],
                bundle,
                type: 'clear_output',
            });
        };
        const displayDataCallback = (data, metadata, transient) => {
            const bundle = {
                data: this.formatResult(data),
                metadata: this.formatResult(metadata),
                transient: this.formatResult(transient),
            };
            postMessage({
                parentHeader: this.formatResult(this._kernel._parent_header)['header'],
                bundle,
                type: 'display_data',
            });
        };
        const updateDisplayDataCallback = (data, metadata, transient) => {
            const bundle = {
                data: this.formatResult(data),
                metadata: this.formatResult(metadata),
                transient: this.formatResult(transient),
            };
            postMessage({
                parentHeader: this.formatResult(this._kernel._parent_header)['header'],
                bundle,
                type: 'update_display_data',
            });
        };
        const publishStreamCallback = (name, text) => {
            const bundle = {
                name: this.formatResult(name),
                text: this.formatResult(text),
            };
            postMessage({
                parentHeader: this.formatResult(this._kernel._parent_header)['header'],
                bundle,
                type: 'stream',
            });
        };
        this._stdout_stream.publish_stream_callback = publishStreamCallback;
        this._stderr_stream.publish_stream_callback = publishStreamCallback;
        this._interpreter.display_pub.clear_output_callback = clearOutputCallback;
        this._interpreter.display_pub.display_data_callback = displayDataCallback;
        this._interpreter.display_pub.update_display_data_callback =
            updateDisplayDataCallback;
        this._interpreter.displayhook.publish_execution_result = publishExecutionResult;
        this._interpreter.input = this.input.bind(this);
        this._interpreter.getpass = this.getpass.bind(this);
        const res = await this._kernel.run(content.code);
        const results = this.formatResult(res);
        if (results['status'] === 'error') {
            publishExecutionError(results['ename'], results['evalue'], results['traceback']);
        }
        return results;
    }
    /**
     * Complete the code submitted by a user.
     *
     * @param content The incoming message with the code to complete.
     */
    async complete(content, parent) {
        await this.setup(parent);
        const res = this._kernel.complete(content.code, content.cursor_pos);
        const results = this.formatResult(res);
        return results;
    }
    /**
     * Inspect the code submitted by a user.
     *
     * @param content The incoming message with the code to inspect.
     */
    async inspect(content, parent) {
        await this.setup(parent);
        const res = this._kernel.inspect(content.code, content.cursor_pos, content.detail_level);
        const results = this.formatResult(res);
        return results;
    }
    /**
     * Check code for completeness submitted by a user.
     *
     * @param content The incoming message with the code to check.
     */
    async isComplete(content, parent) {
        await this.setup(parent);
        const res = this._kernel.is_complete(content.code);
        const results = this.formatResult(res);
        return results;
    }
    /**
     * Respond to the commInfoRequest.
     *
     * @param content The incoming message with the comm target name.
     */
    async commInfo(content, parent) {
        await this.setup(parent);
        const res = this._kernel.comm_info(content.target_name);
        const results = this.formatResult(res);
        return {
            comms: results,
            status: 'ok',
        };
    }
    /**
     * Respond to the commOpen.
     *
     * @param content The incoming message with the comm open.
     */
    async commOpen(content, parent) {
        await this.setup(parent);
        const res = this._kernel.comm_manager.comm_open(this._pyodide.toPy(content));
        const results = this.formatResult(res);
        return results;
    }
    /**
     * Respond to the commMsg.
     *
     * @param content The incoming message with the comm msg.
     */
    async commMsg(content, parent) {
        await this.setup(parent);
        const res = this._kernel.comm_manager.comm_msg(this._pyodide.toPy(content));
        const results = this.formatResult(res);
        return results;
    }
    /**
     * Respond to the commClose.
     *
     * @param content The incoming message with the comm close.
     */
    async commClose(content, parent) {
        await this.setup(parent);
        const res = this._kernel.comm_manager.comm_close(this._pyodide.toPy(content));
        const results = this.formatResult(res);
        return results;
    }
    /**
     * Resolve the input request by getting back the reply from the main thread
     *
     * @param content The incoming message with the reply
     */
    async inputReply(content, parent) {
        await this.setup(parent);
        this._resolveInputReply(content);
    }
    /**
     * Send a input request to the front-end.
     *
     * @param prompt the text to show at the prompt
     * @param password Is the request for a password?
     */
    async sendInputRequest(prompt, password) {
        const content = {
            prompt,
            password,
        };
        postMessage({
            type: 'input_request',
            parentHeader: this.formatResult(this._kernel._parent_header)['header'],
            content,
        });
    }
    async getpass(prompt) {
        prompt = typeof prompt === 'undefined' ? '' : prompt;
        await this.sendInputRequest(prompt, true);
        const replyPromise = new Promise((resolve) => {
            this._resolveInputReply = resolve;
        });
        const result = await replyPromise;
        return result['value'];
    }
    async input(prompt) {
        prompt = typeof prompt === 'undefined' ? '' : prompt;
        await this.sendInputRequest(prompt, false);
        const replyPromise = new Promise((resolve) => {
            this._resolveInputReply = resolve;
        });
        const result = await replyPromise;
        return result['value'];
    }
    /**
     * Send a comm message to the front-end.
     *
     * @param type The type of the comm message.
     * @param content The content.
     * @param metadata The metadata.
     * @param ident The ident.
     * @param buffers The binary buffers.
     */
    async sendComm(type, content, metadata, ident, buffers) {
        postMessage({
            type: type,
            content: this.formatResult(content),
            metadata: this.formatResult(metadata),
            ident: this.formatResult(ident),
            buffers: this.formatResult(buffers),
            parentHeader: this.formatResult(this._kernel._parent_header)['header'],
        });
    }
    /**
     * Initialization options.
     */
    _options = null;
    /**
     * A promise that resolves when all initiaization is complete.
     */
    _initialized;
    _initializer = null;
    /** TODO: real typing */
    _localPath = '';
    _driveName = '';
    _pyodide;
    _kernel;
    _interpreter;
    _stdout_stream;
    _stderr_stream;
    _resolveInputReply;
}


/***/ })

}]);
//# sourceMappingURL=jupyter_ui_packages_lite_ipykernel_lib_worker_js.b416443d66a2168d0ea2.js.map