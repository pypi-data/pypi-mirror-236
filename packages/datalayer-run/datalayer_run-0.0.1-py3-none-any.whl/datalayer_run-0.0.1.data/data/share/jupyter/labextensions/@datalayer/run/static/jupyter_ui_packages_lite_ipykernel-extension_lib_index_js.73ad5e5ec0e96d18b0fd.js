"use strict";
(self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || []).push([["jupyter_ui_packages_lite_ipykernel-extension_lib_index_js"],{

/***/ "../../jupyter/ui/packages/lite/ipykernel-extension/lib/index.js":
/*!***********************************************************************!*\
  !*** ../../jupyter/ui/packages/lite/ipykernel-extension/lib/index.js ***!
  \***********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @datalayer/jupyterlite-server */ "../../jupyter/ui/packages/lite/server/lib/tokens.js");
/* harmony import */ var _datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @datalayer/jupyterlite-kernel */ "../../jupyter/ui/packages/lite/kernel/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The default CDN fallback for Pyodide
 */
const PYODIDE_CDN_URL = 'https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js';
/**
 * The id for the extension, and key in the litePlugins.
 */
const PLUGIN_ID = '@datalayer/jupyterlite-ipykernel-extension:kernel';
/**
 * A plugin to register the Pyodide kernel.
 */
const kernel = {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [_datalayer_jupyterlite_kernel__WEBPACK_IMPORTED_MODULE_1__.IKernelSpecs, _datalayer_jupyterlite_server__WEBPACK_IMPORTED_MODULE_2__.IServiceWorkerRegistrationWrapper],
    activate: (app, kernelspecs, serviceWorkerRegistrationWrapper) => {
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getBaseUrl();
        const config = JSON.parse(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('litePluginSettings') || '{}')[PLUGIN_ID] || {};
        const url = config.pyodideUrl || PYODIDE_CDN_URL;
        const pyodideUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.parse(url).href;
        const rawPipUrls = config.pipliteUrls || [];
        const pipliteUrls = rawPipUrls.map((pipUrl) => _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.parse(pipUrl).href);
        const disablePyPIFallback = !!config.disablePyPIFallback;
        kernelspecs.register({
            spec: {
                name: 'python',
                display_name: 'Python (Pyodide)',
                language: 'python',
                argv: [],
                resources: {
                    'logo-32x32': 'TODO',
                    'logo-64x64': _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(baseUrl, '/kernelspecs/python.png'),
                },
            },
            create: async (options) => {
                const { PyoliteKernel } = await Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_comlink_dist_esm_comlink_mjs"), __webpack_require__.e("jupyter_ui_packages_lite_ipykernel_lib_worker_js"), __webpack_require__.e("jupyter_ui_packages_lite_ipykernel_lib_index_js")]).then(__webpack_require__.bind(__webpack_require__, /*! @datalayer/jupyterlite-ipykernel */ "../../jupyter/ui/packages/lite/ipykernel/lib/index.js"));
                return new PyoliteKernel({
                    ...options,
                    pyodideUrl,
                    pipliteUrls,
                    disablePyPIFallback,
                    mountDrive: serviceWorkerRegistrationWrapper.enabled,
                });
            },
        });
    },
};
const plugins = [kernel];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


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


/***/ })

}]);
//# sourceMappingURL=jupyter_ui_packages_lite_ipykernel-extension_lib_index_js.73ad5e5ec0e96d18b0fd.js.map