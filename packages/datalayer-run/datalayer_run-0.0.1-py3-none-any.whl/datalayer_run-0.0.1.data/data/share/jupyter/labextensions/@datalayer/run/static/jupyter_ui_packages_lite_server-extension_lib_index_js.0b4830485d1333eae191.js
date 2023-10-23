"use strict";
(self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || []).push([["jupyter_ui_packages_lite_server-extension_lib_index_js"],{

/***/ "../../jupyter/ui/packages/lite/kernel/lib/kernels.js":
/*!************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/kernel/lib/kernels.js ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Kernels": () => (/* binding */ Kernels)
/* harmony export */ });
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services/lib/kernel/serialize */ "../../../node_modules/@jupyterlab/services/lib/kernel/serialize.js");
/* harmony import */ var _jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var mock_socket__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! mock-socket */ "../../../node_modules/mock-socket/dist/mock-socket.js");
/* harmony import */ var mock_socket__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(mock_socket__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var async_mutex__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! async-mutex */ "../../../node_modules/async-mutex/index.mjs");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__);






/**
 * A class to handle requests to /api/kernels
 */
class Kernels {
    /**
     * Construct a new Kernels
     *
     * @param options The instantiation options
     */
    constructor(options) {
        const { kernelspecs } = options;
        this._kernelspecs = kernelspecs;
    }
    /**
     * Start a new kernel.
     *
     * @param options The kernel start options.
     */
    async startNew(options) {
        const { id, name, location } = options;
        const factory = this._kernelspecs.factories.get(name);
        // bail if there is no factory associated with the requested kernel
        if (!factory) {
            return { id, name };
        }
        // create a synchronization mechanism to allow only one message
        // to be processed at a time
        const mutex = new async_mutex__WEBPACK_IMPORTED_MODULE_4__.Mutex();
        // hook a new client to a kernel
        const hook = (kernelId, clientId, socket) => {
            const kernel = this._kernels.get(kernelId);
            if (!kernel) {
                throw Error(`No kernel ${kernelId}`);
            }
            this._clients.set(clientId, socket);
            this._kernelClients.get(kernelId)?.add(clientId);
            const processMsg = async (msg) => {
                await mutex.runExclusive(async () => {
                    await kernel.handleMessage(msg);
                });
            };
            socket.on('message', async (message) => {
                let msg;
                if (message instanceof ArrayBuffer) {
                    message = new Uint8Array(message).buffer;
                    msg = (0,_jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__.deserialize)(message, 'v1.kernel.websocket.jupyter.org');
                }
                else if (typeof message === 'string') {
                    const enc = new TextEncoder();
                    const mb = enc.encode(message);
                    msg = (0,_jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__.deserialize)(mb, 'v1.kernel.websocket.jupyter.org');
                }
                else {
                    return;
                }
                // TODO Find a better solution for this?
                // input-reply is asynchronous, must not be processed like other messages
                if (msg.header.msg_type === 'input_reply') {
                    kernel.handleMessage(msg);
                }
                else {
                    void processMsg(msg);
                }
            });
            const removeClient = () => {
                this._clients.delete(clientId);
                this._kernelClients.get(kernelId)?.delete(clientId);
            };
            kernel.disposed.connect(removeClient);
            // TODO: check whether this is called
            // https://github.com/thoov/mock-socket/issues/298
            // https://github.com/jupyterlab/jupyterlab/blob/6bc884a7a8ed73c615ce72ba097bdb790482b5bf/packages/services/src/kernel/default.ts#L1245
            socket.onclose = removeClient;
        };
        // ensure kernel id
        const kernelId = id ?? _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.UUID.uuid4();
        // There is one server per kernel which handles multiple clients
        const kernelUrl = `${Kernels.WS_BASE_URL}api/kernels/${kernelId}/channels`;
        const runningKernel = this._kernels.get(kernelId);
        if (runningKernel) {
            return {
                id: runningKernel.id,
                name: runningKernel.name,
            };
        }
        // start the kernel
        const sendMessage = (msg) => {
            const clientId = msg.header.session;
            const socket = this._clients.get(clientId);
            if (!socket) {
                console.warn(`Trying to send message on removed socket for kernel ${kernelId}`);
                return;
            }
            const message = (0,_jupyterlab_services_lib_kernel_serialize__WEBPACK_IMPORTED_MODULE_1__.serialize)(msg, 'v1.kernel.websocket.jupyter.org');
            // process iopub messages
            if (msg.channel === 'iopub') {
                const clients = this._kernelClients.get(kernelId);
                clients?.forEach((id) => {
                    this._clients.get(id)?.send(message);
                });
                return;
            }
            socket.send(message);
        };
        const kernel = await factory({
            id: kernelId,
            sendMessage,
            name,
            location,
        });
        await kernel.ready;
        this._kernels.set(kernelId, kernel);
        this._kernelClients.set(kernelId, new Set());
        // create the websocket server for the kernel
        const wsServer = new mock_socket__WEBPACK_IMPORTED_MODULE_3__.Server(kernelUrl);
        wsServer.on('connection', (socket) => {
            const url = new URL(socket.url);
            const clientId = url.searchParams.get('session_id') ?? '';
            hook(kernelId, clientId, socket);
        });
        // clean up closed connection
        wsServer.on('close', () => {
            this._clients.keys().forEach((clientId) => {
                const socket = this._clients.get(clientId);
                if (socket?.readyState === WebSocket.CLOSED) {
                    this._clients.delete(clientId);
                    this._kernelClients.get(kernelId)?.delete(clientId);
                }
            });
        });
        // cleanup on kernel shutdown
        kernel.disposed.connect(() => {
            wsServer.close();
            this._kernels.delete(kernelId);
            this._kernelClients.delete(kernelId);
        });
        return {
            id: kernel.id,
            name: kernel.name,
        };
    }
    /**
     * Restart a kernel.
     *
     * @param kernelId The kernel id.
     */
    async restart(kernelId) {
        const kernel = this._kernels.get(kernelId);
        if (!kernel) {
            throw Error(`Kernel ${kernelId} does not exist`);
        }
        const { id, name, location } = kernel;
        kernel.dispose();
        return this.startNew({ id, name, location });
    }
    /**
     * Shut down a kernel.
     *
     * @param id The kernel id.
     */
    async shutdown(id) {
        this._kernels.delete(id)?.dispose();
    }
    _kernels = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableMap();
    _clients = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableMap();
    _kernelClients = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableMap();
    _kernelspecs;
}
/**
 * A namespace for Kernels statics.
 */
(function (Kernels) {
    /**
     * The base url for the Kernels manager
     */
    Kernels.WS_BASE_URL = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PageConfig.getBaseUrl().replace(/^http/, 'ws');
})(Kernels || (Kernels = {}));


/***/ }),

/***/ "../../jupyter/ui/packages/lite/kernel/lib/kernelspecs.js":
/*!****************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/kernel/lib/kernelspecs.js ***!
  \****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelSpecs": () => (/* binding */ KernelSpecs)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../../jupyter/ui/packages/lite/kernel/lib/tokens.js");


/**
 * A class to handle requests to /api/kernelspecs
 */
class KernelSpecs {
    /**
     * Get the kernel specs.
     */
    get specs() {
        if (this._specs.size === 0) {
            return null;
        }
        return {
            default: this.defaultKernelName,
            kernelspecs: Object.fromEntries(this._specs),
        };
    }
    /**
     * Get the default kernel name.
     */
    get defaultKernelName() {
        let defaultKernelName = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('defaultKernelName');
        if (!defaultKernelName && this._specs.size) {
            const keys = Array.from(this._specs.keys());
            keys.sort();
            defaultKernelName = keys[0];
        }
        return defaultKernelName || _tokens__WEBPACK_IMPORTED_MODULE_1__.FALLBACK_KERNEL;
    }
    /**
     * Get the kernel factories for the current kernels.
     */
    get factories() {
        return this._factories;
    }
    /**
     * Register a new kernel.
     *
     * @param options The options to register a new kernel.
     */
    register(options) {
        const { spec, create } = options;
        this._specs.set(spec.name, spec);
        this._factories.set(spec.name, create);
    }
    _specs = new Map();
    _factories = new Map();
}


/***/ }),

/***/ "../../jupyter/ui/packages/lite/kernel/lib/tokens.js":
/*!***********************************************************!*\
  !*** ../../jupyter/ui/packages/lite/kernel/lib/tokens.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FALLBACK_KERNEL": () => (/* binding */ FALLBACK_KERNEL),
/* harmony export */   "IKernelSpecs": () => (/* binding */ IKernelSpecs),
/* harmony export */   "IKernels": () => (/* binding */ IKernels)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The token for the kernels service.
 */
const IKernels = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyterlite-kernel:IKernels');
/**
 * The kernel name of last resort.
 */
const FALLBACK_KERNEL = 'javascript';
/**
 * The token for the kernel spec service.
 */
const IKernelSpecs = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyterlite-kernel:IKernelSpecs');


/***/ }),

/***/ "../../jupyter/ui/packages/lite/server-extension/lib/index.js":
/*!********************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/server-extension/lib/index.js ***!
  \********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @datalayer/jupyterlite-kernel */ "../../jupyter/ui/packages/lite/kernel/lib/tokens.js");
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @datalayer/jupyterlite-kernel */ "../../jupyter/ui/packages/lite/kernel/lib/kernels.js");
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @datalayer/jupyterlite-kernel */ "../../jupyter/ui/packages/lite/kernel/lib/kernelspecs.js");
/* harmony import */ var _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @datalayer/jupyterlite-server */ "../../jupyter/ui/packages/lite/server/lib/tokens.js");
/* harmony import */ var _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @datalayer/jupyterlite-server */ "../../jupyter/ui/packages/lite/server/lib/serviceworker.js");
/* harmony import */ var _datalayer_jupyterlite_session__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @datalayer/jupyterlite-session */ "../../jupyter/ui/packages/lite/session/lib/tokens.js");
/* harmony import */ var _datalayer_jupyterlite_session__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @datalayer/jupyterlite-session */ "../../jupyter/ui/packages/lite/session/lib/sessions.js");
/* harmony import */ var _datalayer_jupyterlite_settings__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @datalayer/jupyterlite-settings */ "../../jupyter/ui/packages/lite/settings/lib/tokens.js");
/* harmony import */ var _datalayer_jupyterlite_settings__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @datalayer/jupyterlite-settings */ "../../jupyter/ui/packages/lite/settings/lib/settings.js");
/* harmony import */ var localforage__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! localforage */ "../../../node_modules/localforage/dist/localforage.js");
/* harmony import */ var localforage__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(localforage__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * A plugin installing the service worker.
 */
const serviceWorkerPlugin = {
    id: '@datalayer/jupyterlite-server-extension:service-worker',
    autoStart: true,
    provides: _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_2__.IServiceWorkerRegistrationWrapper,
    activate: (app) => {
        return new _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_3__.ServiceWorkerRegistrationWrapper();
    },
};
/**
 * The kernels service plugin.
 */
const kernelsPlugin = {
    id: '@datalayer/jupyterlite-server-extension:kernels',
    autoStart: true,
    provides: _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_4__.IKernels,
    requires: [_datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_4__.IKernelSpecs],
    activate: (app, kernelspecs) => {
        return new _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_5__.Kernels({ kernelspecs });
    },
};
/**
 * A plugin providing the routes for the kernels service
 */
const kernelsRoutesPlugin = {
    id: '@datalayer/jupyterlite-server-extension:kernels-routes',
    autoStart: true,
    requires: [_datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_4__.IKernels],
    activate: (app, kernels) => {
        // POST /api/kernels/{kernel_id} - Restart a kernel
        app.router.post('/api/kernels/(.*)/restart', async (req, kernelId) => {
            const res = await kernels.restart(kernelId);
            return new Response(JSON.stringify(res));
        });
        // DELETE /api/kernels/{kernel_id} - Kill a kernel and delete the kernel id
        app.router.delete('/api/kernels/(.*)', async (req, kernelId) => {
            const res = await kernels.shutdown(kernelId);
            return new Response(JSON.stringify(res), { status: 204 });
        });
    },
};
/**
 * The kernel spec service plugin.
 */
const kernelSpecPlugin = {
    id: '@datalayer/jupyterlite-server-extension:kernelspec',
    autoStart: true,
    provides: _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_4__.IKernelSpecs,
    activate: (app) => {
        return new _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_6__.KernelSpecs();
    },
};
/**
 * A plugin providing the routes for the kernelspec service.
 */
const kernelSpecRoutesPlugin = {
    id: '@datalayer/jupyterlite-server-extension:kernelspec-routes',
    autoStart: true,
    requires: [_datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_4__.IKernelSpecs],
    activate: (app, kernelspecs) => {
        app.router.get('/api/kernelspecs', async (req) => {
            const { specs } = kernelspecs;
            if (!specs) {
                return new Response(null);
            }
            // follow the same format as in Jupyter Server
            const allKernelSpecs = {};
            const allSpecs = specs.kernelspecs;
            Object.keys(allSpecs).forEach((name) => {
                const spec = allSpecs[name];
                const { resources } = spec ?? {};
                allKernelSpecs[name] = {
                    name,
                    spec,
                    resources,
                };
            });
            const res = {
                default: specs.default,
                kernelspecs: allKernelSpecs,
            };
            return new Response(JSON.stringify(res));
        });
    },
};
/**
 * A plugin providing the routes for the nbconvert service.
 * TODO: provide the service in a separate plugin?
 */
const nbconvertRoutesPlugin = {
    id: '@datalayer/jupyterlite-server-extension:nbconvert-routes',
    autoStart: true,
    activate: (app) => {
        app.router.get('/api/nbconvert', async (req) => {
            return new Response(JSON.stringify({}));
        });
    },
};
/**
 * The sessions service plugin.
 */
const sessionsPlugin = {
    id: '@datalayer/jupyterlite-server-extension:sessions',
    autoStart: true,
    provides: _datalayer_jupyterlite_session__WEBPACK_IMPORTED_MODULE_7__.ISessions,
    requires: [_datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_4__.IKernels],
    activate: (app, kernels) => {
        return new _datalayer_jupyterlite_session__WEBPACK_IMPORTED_MODULE_8__.Sessions({ kernels });
    },
};
/**
 * A plugin providing the routes for the session service.
 */
const sessionsRoutesPlugin = {
    id: '@datalayer/jupyterlite-server-extension:sessions-routes',
    autoStart: true,
    requires: [_datalayer_jupyterlite_session__WEBPACK_IMPORTED_MODULE_7__.ISessions],
    activate: (app, sessions) => {
        // GET /api/sessions/{session} - Get session
        app.router.get('/api/sessions/(.+)', async (req, id) => {
            const session = await sessions.get(id);
            return new Response(JSON.stringify(session), { status: 200 });
        });
        // GET /api/sessions - List available sessions
        app.router.get('/api/sessions', async (req) => {
            const list = await sessions.list();
            return new Response(JSON.stringify(list), { status: 200 });
        });
        // PATCH /api/sessions/{session} - This can be used to rename a session
        app.router.patch('/api/sessions(.*)', async (req, id) => {
            const options = req.body;
            const session = await sessions.patch(options);
            return new Response(JSON.stringify(session), { status: 200 });
        });
        // DELETE /api/sessions/{session} - Delete a session
        app.router.delete('/api/sessions/(.+)', async (req, id) => {
            await sessions.shutdown(id);
            return new Response(null, { status: 204 });
        });
        // POST /api/sessions - Create a new session or return an existing session if a session of the same name already exists
        app.router.post('/api/sessions', async (req) => {
            const options = req.body;
            const session = await sessions.startNew(options);
            return new Response(JSON.stringify(session), { status: 201 });
        });
    },
};
/**
 * The settings service plugin.
 */
const settingsPlugin = {
    id: '@datalayer/jupyterlite-server-extension:settings',
    autoStart: true,
    requires: [],
    provides: _datalayer_jupyterlite_settings__WEBPACK_IMPORTED_MODULE_9__.ISettings,
    activate: (app) => {
        const storageName = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('settingsStorageName');
        const storageDrivers = JSON.parse(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('settingsStorageDrivers') || 'null');
        const settings = new _datalayer_jupyterlite_settings__WEBPACK_IMPORTED_MODULE_10__.Settings({ storageName, storageDrivers, localforage: (localforage__WEBPACK_IMPORTED_MODULE_1___default()) });
        app.started.then(() => settings.initialize().catch(console.warn));
        return settings;
    },
};
/**
 * A plugin providing the routes for the settings service.
 */
const settingsRoutesPlugin = {
    id: '@datalayer/jupyterlite-server-extension:settings-routes',
    autoStart: true,
    requires: [_datalayer_jupyterlite_settings__WEBPACK_IMPORTED_MODULE_9__.ISettings],
    activate: (app, settings) => {
        // TODO: improve the regex
        // const pluginPattern = new RegExp(/(?:@([^/]+?)[/])?([^/]+?):(\w+)/);
        const pluginPattern = '/api/settings/((?:@([^/]+?)[/])?([^/]+?):([^:]+))$';
        app.router.get(pluginPattern, async (req, pluginId) => {
            const setting = await settings.get(pluginId);
            return new Response(JSON.stringify(setting));
        });
        app.router.put(pluginPattern, async (req, pluginId) => {
            const body = req.body;
            const { raw } = body;
            await settings.save(pluginId, raw);
            return new Response(null, { status: 204 });
        });
        app.router.get('/api/settings', async (req) => {
            const plugins = await settings.getAll();
            return new Response(JSON.stringify(plugins));
        });
    },
};
const plugins = [
    kernelsPlugin,
    kernelsRoutesPlugin,
    kernelSpecPlugin,
    kernelSpecRoutesPlugin,
    nbconvertRoutesPlugin,
    serviceWorkerPlugin,
    sessionsPlugin,
    sessionsRoutesPlugin,
    settingsPlugin,
    settingsRoutesPlugin,
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "../../jupyter/ui/packages/lite/server/lib/serviceworker.js":
/*!******************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/server/lib/serviceworker.js ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ServiceWorkerRegistrationWrapper": () => (/* binding */ ServiceWorkerRegistrationWrapper)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);

class ServiceWorkerRegistrationWrapper {
    constructor() {
        this.initialize();
    }
    /**
     * A signal emitted when the registration changes.
     */
    get registrationChanged() {
        return this._registrationChanged;
    }
    /**
     * Whether the ServiceWorker is enabled or not.
     */
    get enabled() {
        return this._registration !== null;
    }
    async initialize() {
        if (!('serviceWorker' in navigator)) {
            console.error('ServiceWorker registration failed: Service Workers not supported in this browser');
            this.setRegistration(null);
        }
        if (navigator.serviceWorker.controller) {
            const registration = await navigator.serviceWorker.getRegistration(navigator.serviceWorker.controller.scriptURL);
            if (registration) {
                this.setRegistration(registration);
            }
        }
        return await navigator.serviceWorker
            //      .register(URLExt.join(PageConfig.getBaseUrl(), 'services.js'))
            .register("/services.js")
            .then((registration) => {
            this.setRegistration(registration);
        }, (err) => {
            console.error(`ServiceWorker registration failed: ${err}`);
            this.setRegistration(null);
        });
    }
    setRegistration(registration) {
        this._registration = registration;
        this._registrationChanged.emit(this._registration);
    }
    _registration = null;
    _registrationChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
}


/***/ }),

/***/ "../../jupyter/ui/packages/lite/server/lib/tokens.js":
/*!***********************************************************!*\
  !*** ../../jupyter/ui/packages/lite/server/lib/tokens.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IServiceWorkerRegistrationWrapper": () => (/* binding */ IServiceWorkerRegistrationWrapper)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The token for the ServiceWorker.
 */
const IServiceWorkerRegistrationWrapper = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyterlite-server-extension:IServiceWorkerRegistrationWrapper');


/***/ }),

/***/ "../../jupyter/ui/packages/lite/session/lib/sessions.js":
/*!**************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/session/lib/sessions.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Sessions": () => (/* binding */ Sessions)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);



/**
 * A class to handle requests to /api/sessions
 */
class Sessions {
    /**
     * Construct a new Sessions.
     *
     * @param options The instantiation options for a Sessions.
     */
    constructor(options) {
        this._kernels = options.kernels;
    }
    /**
     * Get a session by id.
     *
     * @param id The id of the session.
     */
    async get(id) {
        const session = this._sessions.find((s) => s.id === id);
        if (!session) {
            throw Error(`Session ${id} not found`);
        }
        return session;
    }
    /**
     * List the running sessions
     */
    async list() {
        return this._sessions;
    }
    /**
     * Path an existing session.
     * This can be used to rename a session.
     * TODO: read path and name
     *
     * @param options The options to patch the session.
     */
    async patch(options) {
        const { id, path, name } = options;
        const index = this._sessions.findIndex((s) => s.id === id);
        const session = this._sessions[index];
        if (!session) {
            throw Error(`Session ${id} not found`);
        }
        const patched = {
            ...session,
            path: path ?? session.path,
            name: name ?? session.name,
        };
        this._sessions[index] = patched;
        return patched;
    }
    /**
     * Start a new session
     * TODO: read path and name
     *
     * @param options The options to start a new session.
     */
    async startNew(options) {
        const { path, name } = options;
        const running = this._sessions.find((s) => s.name === name);
        if (running) {
            return running;
        }
        const kernelName = options.kernel?.name ?? '';
        const id = options.id ?? _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.UUID.uuid4();
        const kernel = await this._kernels.startNew({
            id,
            name: kernelName,
            location: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.dirname(options.path),
        });
        const session = {
            id,
            path,
            name: name ?? path,
            type: 'notebook',
            kernel: {
                id: kernel.id,
                name: kernel.name,
            },
        };
        this._sessions.push(session);
        return session;
    }
    /**
     * Shut down a session.
     *
     * @param id The id of the session to shut down.
     */
    async shutdown(id) {
        const session = this._sessions.find((s) => s.id === id);
        if (!session) {
            throw Error(`Session ${id} not found`);
        }
        const kernelId = session.kernel?.id;
        if (kernelId) {
            await this._kernels.shutdown(kernelId);
        }
        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.removeFirstOf(this._sessions, session);
    }
    _kernels;
    // TODO: offload to a database
    _sessions = [];
}


/***/ }),

/***/ "../../jupyter/ui/packages/lite/session/lib/tokens.js":
/*!************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/session/lib/tokens.js ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ISessions": () => (/* binding */ ISessions)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The token for the sessions service.
 */
const ISessions = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyterlite-session:ISessions');


/***/ }),

/***/ "../../jupyter/ui/packages/lite/settings/lib/settings.js":
/*!***************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/settings/lib/settings.js ***!
  \***************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Settings": () => (/* binding */ Settings)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var json5__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! json5 */ "../../../node_modules/json5/dist/index.js");
/* harmony import */ var json5__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(json5__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);



/**
 * The name of the local storage.
 */
const DEFAULT_STORAGE_NAME = 'JupyterLite Storage';
/**
 * A class to handle requests to /api/settings
 */
class Settings {
    constructor(options) {
        this._localforage = options.localforage;
        this._storageName = options.storageName || DEFAULT_STORAGE_NAME;
        this._storageDrivers = options.storageDrivers || null;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
    }
    /**
     * A promise that resolves when the settings storage is fully initialized
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * A lazy reference to initialized storage
     */
    get storage() {
        return this.ready.then(() => this._storage);
    }
    /**
     * Finish any initialization after server has started and all extensions are applied.
     */
    async initialize() {
        await this.initStorage();
        this._ready.resolve(void 0);
    }
    /**
     * Prepare the storage
     */
    async initStorage() {
        this._storage = this.defaultSettingsStorage();
    }
    /**
     * Get default options for localForage instances
     */
    get defaultStorageOptions() {
        const driver = this._storageDrivers?.length ? this._storageDrivers : null;
        return {
            version: 1,
            name: this._storageName,
            ...(driver ? { driver } : {}),
        };
    }
    /**
     * Create a settings store.
     */
    defaultSettingsStorage() {
        return this._localforage.createInstance({
            description: 'Offline Storage for Settings',
            storeName: 'settings',
            ...this.defaultStorageOptions,
        });
    }
    /**
     * Get settings by plugin id
     *
     * @param pluginId the id of the plugin
     *
     */
    async get(pluginId) {
        const all = await this.getAll();
        const settings = all.settings;
        let found = settings.find((setting) => {
            return setting.id === pluginId;
        });
        if (!found) {
            found = await this._getFederated(pluginId);
        }
        return found;
    }
    /**
     * Get all the settings
     */
    async getAll() {
        const settingsUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('settingsUrl') ?? '/';
        const storage = await this.storage;
        const all = (await (await fetch(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settingsUrl, 'all.json'))).json());
        const settings = await Promise.all(all.map(async (plugin) => {
            const { id } = plugin;
            const raw = (await storage.getItem(id)) ?? plugin.raw;
            return {
                ...Private.override(plugin),
                raw,
                settings: json5__WEBPACK_IMPORTED_MODULE_1__.parse(raw),
            };
        }));
        return { settings };
    }
    /**
     * Save settings for a given plugin id
     *
     * @param pluginId The id of the plugin
     * @param raw The raw settings
     *
     */
    async save(pluginId, raw) {
        await (await this.storage).setItem(pluginId, raw);
    }
    /**
     * Get the settings for a federated extension
     *
     * @param pluginId The id of a plugin
     */
    async _getFederated(pluginId) {
        const [packageName, schemaName] = pluginId.split(':');
        if (!Private.isFederated(packageName)) {
            return;
        }
        const labExtensionsUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('fullLabextensionsUrl');
        const schemaUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(labExtensionsUrl, packageName, 'schemas', packageName, `${schemaName}.json`);
        const packageUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(labExtensionsUrl, packageName, 'package.json');
        const schema = await (await fetch(schemaUrl)).json();
        const packageJson = await (await fetch(packageUrl)).json();
        const raw = (await (await this.storage).getItem(pluginId)) ?? '{}';
        const settings = json5__WEBPACK_IMPORTED_MODULE_1__.parse(raw) || {};
        return Private.override({
            id: pluginId,
            raw,
            schema,
            settings,
            version: packageJson.version || '3.0.8',
        });
    }
    _storageName = DEFAULT_STORAGE_NAME;
    _storageDrivers = null;
    _storage;
    _localforage;
    _ready;
}
/**
 * A namespace for private data
 */
var Private;
(function (Private) {
    const _overrides = JSON.parse(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('settingsOverrides') || '{}');
    /**
     * Test whether this package is configured in `federated_extensions` in this app
     *
     * @param packageName The npm name of a package
     */
    function isFederated(packageName) {
        let federated;
        try {
            federated = JSON.parse(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('federated_extensions'));
        }
        catch {
            return false;
        }
        for (const { name } of federated) {
            if (name === packageName) {
                return true;
            }
        }
        return false;
    }
    Private.isFederated = isFederated;
    /**
     * Override the defaults of the schema with ones from PageConfig
     *
     * @see https://github.com/jupyterlab/jupyterlab_server/blob/v2.5.2/jupyterlab_server/settings_handler.py#L216-L227
     */
    function override(plugin) {
        if (_overrides[plugin.id]) {
            if (!plugin.schema.properties) {
                // probably malformed, or only provides keyboard shortcuts, etc.
                plugin.schema.properties = {};
            }
            for (const [prop, propDefault] of Object.entries(_overrides[plugin.id] || {})) {
                plugin.schema.properties[prop].default = propDefault;
            }
        }
        return plugin;
    }
    Private.override = override;
})(Private || (Private = {}));


/***/ }),

/***/ "../../jupyter/ui/packages/lite/settings/lib/tokens.js":
/*!*************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/settings/lib/tokens.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ISettings": () => (/* binding */ ISettings)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The token for the settings service.
 */
const ISettings = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/jupyterlite-settings:ISettings');


/***/ })

}]);
//# sourceMappingURL=jupyter_ui_packages_lite_server-extension_lib_index_js.0b4830485d1333eae191.js.map