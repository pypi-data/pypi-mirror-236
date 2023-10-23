"use strict";
(self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || []).push([["lib_jupyterlab_index_js"],{

/***/ "../../../node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!*********************************************************************!*\
  !*** ../../../node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \*********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "body {\n  overflow-y: visible;\n}\n\n.dla-Container {\n  overflow-y: visible;\n}\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;EACE,mBAAmB;AACrB;;AAEA;EACE,mBAAmB;AACrB","sourcesContent":["body {\n  overflow-y: visible;\n}\n\n.dla-Container {\n  overflow-y: visible;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../../../node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!**********************************************************************!*\
  !*** ../../../node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \**********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/css-loader/dist/runtime/api.js */ "../../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../../../../node_modules/css-loader/dist/cjs.js!./base.css */ "../../../node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../icons/react/data1/esm/DatalayerGreenPaddingIcon.js":
/*!*************************************************************!*\
  !*** ../icons/react/data1/esm/DatalayerGreenPaddingIcon.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function DatalayerGreenPaddingIcon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    fill: colored ? 'none' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('none') ? 'white' : 'currentColor'),
    "aria-hidden": "true",
    viewBox: "0 0 72 72",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#2ecc71' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#2ecc71') ? 'white' : 'currentColor'),
    strokeWidth: 2.9,
    d: "M7 7h58v11.6H7zm0 0"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#1abc9c' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#1abc9c') ? 'white' : 'currentColor'),
    strokeWidth: 2.9,
    d: "M7 30.2h58v11.6H7zm0 0"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fill: colored ? '#16a085' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#16a085') ? 'white' : 'currentColor'),
    strokeWidth: 2.9,
    d: "M7 53.4h58V65H7zm0 0"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(DatalayerGreenPaddingIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../icons/react/data1/esm/DatalayerGreenPaddingIconJupyterLab.js":
/*!***********************************************************************!*\
  !*** ../icons/react/data1/esm/DatalayerGreenPaddingIconJupyterLab.js ***!
  \***********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components/lib/icon/labicon */ "../../../node_modules/@jupyterlab/ui-components/lib/icon/labicon.js");
/* harmony import */ var _DatalayerGreenPaddingIcon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./DatalayerGreenPaddingIcon.svg */ "../icons/react/data1/esm/DatalayerGreenPaddingIcon.svg");


const datalayerGreenPaddingIconJupyterLab = new _jupyterlab_ui_components_lib_icon_labicon__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: '@datalayer/icons:datalayer-green-padding',
    svgstr: _DatalayerGreenPaddingIcon_svg__WEBPACK_IMPORTED_MODULE_1__,
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (datalayerGreenPaddingIconJupyterLab);

/***/ }),

/***/ "../icons/react/data1/esm/TerminalIcon.js":
/*!************************************************!*\
  !*** ../icons/react/data1/esm/TerminalIcon.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function TerminalIcon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    fill: colored ? 'currentColor' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('currentColor') ? 'white' : 'currentColor'),
    viewBox: "0 0 20 20",
    "aria-hidden": "true",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    d: "M.02 3.471c0-1.207.98-2.187 2.187-2.187h15.625c1.208 0 2.188.98 2.188 2.187v13.125a2.188 2.188 0 01-2.188 2.188H2.207A2.187 2.187 0 01.02 16.596V3.471zm2.187-.312a.312.312 0 00-.312.312v13.125c0 .173.14.313.312.313h15.625a.313.313 0 00.313-.313V3.471a.312.312 0 00-.313-.312H2.207zm6.875 6.875a.937.937 0 01-.275.662L5.995 13.51a.937.937 0 11-1.325-1.325l2.15-2.15-2.15-2.15a.936.936 0 01.903-1.586.936.936 0 01.422.26l2.812 2.813a.933.933 0 01.275.663zm1.875 1.875h3.75a.938.938 0 010 1.875h-3.75a.937.937 0 110-1.875z"
  }));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(TerminalIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "../icons/react/eggs/esm/ECharlesIcon.js":
/*!***********************************************!*\
  !*** ../icons/react/eggs/esm/ECharlesIcon.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);


const sizeMap = {
  "small": 16,
  "medium": 32,
  "large": 64
};

function ECharlesIcon({
  title,
  titleId,
  size,
  colored,
  ...props
}, svgRef) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", Object.assign({
    xmlns: "http://www.w3.org/2000/svg",
    viewBox: "0 0 243.75 243.75",
    fill: colored ? 'currentColor' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('currentColor') ? 'white' : 'currentColor'),
    "aria-hidden": "true",
    width: size ? typeof size === "string" ? sizeMap[size] : size : "16px",
    ref: svgRef,
    "aria-labelledby": titleId
  }, props), title ? /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", {
    id: titleId
  }, title) : null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("g", {
    fill: colored ? '#fff' : (['#fff', '#fffff', 'white', '#FFF', '#FFFFFF'].includes('#fff') ? 'white' : 'currentColor'),
    strokeWidth: 2.928,
    transform: "translate(0 -308.268)"
  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("circle", {
    cx: 121.875,
    cy: 430.143,
    r: 120.411,
    stroke: "#000"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fillRule: "evenodd",
    stroke: "#000",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    d: "M119.675 477.588l.253-140.166c-73.532 5.11-86.696 84.242-28.25 114.7l.61 25.34z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fillRule: "evenodd",
    stroke: "#000",
    d: "M120.07 482.652H93.813c-2.945 4.667-3.575 8.04 2.748 13.127-6.62.865-6.378 8.548-2.9 10.686-4.242 1.556-5.282 8.727 6.869 7.937l1.625 5.486c.733 2.113 1.746 2.545 2.76 2.973l10.458-.086c1.992-.72 4.299-2.105 4.39-5.015z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fillRule: "evenodd",
    stroke: "#f75c59",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    d: "M124.291 477.462l-.469-139.95c73.532 5.11 86.696 84.458 28.25 114.916l-.61 25.34z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fillRule: "evenodd",
    stroke: "#f75c59",
    d: "M125.32 482.957l-.306 32.361c1.317 11.059 11.072 8.629 10.99-.61v-31.751zM139.957 482.957l-.305 32.361c1.317 11.059 11.072 8.629 10.99-.61v-31.751z"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fillRule: "evenodd",
    stroke: "#f8d05b",
    d: "M112.412 477.238l-16.948-73.934c-4.23-19.168-16.974-14.783-11.444-.557 6.267 10.896 28.39 21.763 33.582 6.106-4.523-5.743-6.628-12.59 1.333-16.65"
  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", {
    fillRule: "evenodd",
    stroke: "#f75c59",
    strokeLinejoin: "round",
    d: "M131.627 399.814c1.778-4.471 12.628-9.482 19.487-14.062 7.117 3.213 17.741 13.145 12.804 25.555-1.265 4.901-28.05 4.544-30.224 2.137-4.481-4.606-3.115-10.024-2.067-13.63zM128.198 428.251c-.91 7.576-.577 13.909-.763 20.76 3.425.788 7.262.337 11.082-.062-2.75-6.95-5.704-13.748-10.319-20.698z"
  })));
}
const ForwardRef = react__WEBPACK_IMPORTED_MODULE_0__.forwardRef(ECharlesIcon);
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ForwardRef);

/***/ }),

/***/ "./lib/Run.js":
/*!********************!*\
  !*** ./lib/Run.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/ThemeProvider.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/BaseStyles.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/UnderlineNav2/index.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @datalayer/icons-react */ "../icons/react/data1/esm/DatalayerGreenPaddingIcon.js");
/* harmony import */ var _jupyterlab_handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./jupyterlab/handler */ "./lib/jupyterlab/handler.js");
/* harmony import */ var _state_zustand__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./state/zustand */ "./lib/state/zustand.js");
/* harmony import */ var _tabs_ImagesTab__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/ImagesTab */ "./lib/tabs/ImagesTab.js");
/* harmony import */ var _tabs_ContainersTab__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/ContainersTab */ "./lib/tabs/ContainersTab.js");
/* harmony import */ var _tabs_VolumesTab__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./tabs/VolumesTab */ "./lib/tabs/VolumesTab.js");
/* harmony import */ var _tabs_NetworksTab__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./tabs/NetworksTab */ "./lib/tabs/NetworksTab.js");
/* harmony import */ var _tabs_SecretsTab__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./tabs/SecretsTab */ "./lib/tabs/SecretsTab.js");
/* harmony import */ var _tabs_AboutTab__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./tabs/AboutTab */ "./lib/tabs/AboutTab.js");













const DatalayerRun = (props) => {
    const { setTab, getIntTab } = (0,_state_zustand__WEBPACK_IMPORTED_MODULE_2__["default"])();
    const intTab = getIntTab();
    const [version, setVersion] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_jupyterlab_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('config')
            .then(data => {
            setVersion(data.version);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav, { "aria-label": "run", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav.Item, { "aria-label": "images", "aria-current": intTab === 0 ? "page" : undefined, onSelect: e => { e.preventDefault(); setTab(0.0); }, children: "Images" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav.Item, { "aria-label": "containers", "aria-current": intTab === 1 ? "page" : undefined, onSelect: e => { e.preventDefault(); setTab(1.0); }, children: "Containers" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav.Item, { "aria-label": "containers", "aria-current": intTab === 2 ? "page" : undefined, onSelect: e => { e.preventDefault(); setTab(2.0); }, children: "Volumes" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav.Item, { "aria-label": "containers", "aria-current": intTab === 3 ? "page" : undefined, onSelect: e => { e.preventDefault(); setTab(3.0); }, children: "Networks" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav.Item, { "aria-label": "containers", "aria-current": intTab === 4 ? "page" : undefined, onSelect: e => { e.preventDefault(); setTab(4.0); }, children: "Secrets" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_7__.UnderlineNav.Item, { "aria-label": "about", "aria-current": intTab === 5 ? "page" : undefined, icon: () => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react__WEBPACK_IMPORTED_MODULE_8__["default"], { colored: true }), onSelect: e => { e.preventDefault(); setTab(5.0); }, children: "About" })] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { m: 3, children: [intTab === 0 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_ImagesTab__WEBPACK_IMPORTED_MODULE_9__["default"], {}), intTab === 1 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_ContainersTab__WEBPACK_IMPORTED_MODULE_10__["default"], {}), intTab === 2 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_VolumesTab__WEBPACK_IMPORTED_MODULE_11__["default"], {}), intTab === 3 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_NetworksTab__WEBPACK_IMPORTED_MODULE_12__["default"], {}), intTab === 4 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_SecretsTab__WEBPACK_IMPORTED_MODULE_13__["default"], {}), intTab === 5 && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_tabs_AboutTab__WEBPACK_IMPORTED_MODULE_14__["default"], { version: version })] })] }) }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DatalayerRun);


/***/ }),

/***/ "./lib/jupyterlab/handler.js":
/*!***********************************!*\
  !*** ./lib/jupyterlab/handler.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'datalayer_run', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/jupyterlab/index.js":
/*!*********************************!*\
  !*** ./lib/jupyterlab/index.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IDatalayerRun": () => (/* binding */ IDatalayerRun),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _datalayer_icons_react_data1_DatalayerGreenPaddingIconJupyterLab__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @datalayer/icons-react/data1/DatalayerGreenPaddingIconJupyterLab */ "../icons/react/data1/esm/DatalayerGreenPaddingIconJupyterLab.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./handler */ "./lib/jupyterlab/handler.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./widget */ "./lib/jupyterlab/widget.js");
/* harmony import */ var _state_zustand__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../state/zustand */ "./lib/state/zustand.js");
/* harmony import */ var _state_mobx__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../state/mobx */ "./lib/state/mobx.js");
/* harmony import */ var _timer_TimerView__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../timer/TimerView */ "./lib/timer/TimerView.js");
/* harmony import */ var _service_DatalayerServiceManager__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./service/DatalayerServiceManager */ "./lib/jupyterlab/service/DatalayerServiceManager.js");
/* harmony import */ var _local_drive__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./local-drive */ "./lib/jupyterlab/local-drive/index.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../style/index.css */ "./style/index.css");















const IDatalayerRun = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@datalayer/run:plugin');
const sessionDialogs = {
    id: '@datalayer/apputils-extension:sessionDialogs',
    description: 'Provides the session context dialogs.',
    provides: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ISessionContextDialogs,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    autoStart: true,
    activate: async (app, translator) => {
        return new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.SessionContextDialogs({
            translator: translator ?? _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator
        });
    }
};
/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-datalayer-run-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the @datalayer/run extension.
 */
const plugin = {
    id: '@datalayer/run:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_5__.ILauncher, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILayoutRestorer],
    provides: IDatalayerRun,
    activate: (app, palette, settingRegistry, launcher, restorer) => {
        const { commands } = app;
        app.serviceManager = new _service_DatalayerServiceManager__WEBPACK_IMPORTED_MODULE_7__["default"](app.serviceManager);
        const command = CommandIDs.create;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.WidgetTracker({
            namespace: 'datalayer-run',
        });
        if (restorer) {
            void restorer.restore(tracker, {
                command,
                name: () => 'datalayer-run',
            });
        }
        const datalayerRun = {
            timer: new _state_zustand__WEBPACK_IMPORTED_MODULE_8__.Timer(),
            TimerView: _timer_TimerView__WEBPACK_IMPORTED_MODULE_9__.TimerView,
            mobxTimer: _state_mobx__WEBPACK_IMPORTED_MODULE_10__.mobxTimer,
            MobxTimerView: _state_mobx__WEBPACK_IMPORTED_MODULE_10__.MobxTimerView,
        };
        commands.addCommand(command, {
            caption: 'Show Datalayer Run',
            label: 'Datalayer Run',
            icon: _datalayer_icons_react_data1_DatalayerGreenPaddingIconJupyterLab__WEBPACK_IMPORTED_MODULE_11__["default"],
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_12__.DatalayerRunWidget(app, datalayerRun);
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.MainAreaWidget({ content });
                widget.title.label = 'Datalayer Run';
                widget.title.icon = _datalayer_icons_react_data1_DatalayerGreenPaddingIconJupyterLab__WEBPACK_IMPORTED_MODULE_11__["default"];
                app.shell.add(widget, 'main');
                tracker.add(widget);
            }
        });
        const category = 'Datalayer';
        palette.addItem({ command, category });
        if (launcher) {
            launcher.add({
                command,
                category,
                rank: 1.1,
            });
        }
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('@datalayer/run settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for @datalayer/run.', reason);
            });
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_13__.requestAPI)('config')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
        console.log('JupyterLab plugin @datalayer/run:plugin is activated.');
        return datalayerRun;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
    plugin,
    sessionDialogs,
    _local_drive__WEBPACK_IMPORTED_MODULE_14__["default"],
]);


/***/ }),

/***/ "./lib/jupyterlab/local-drive/drive.js":
/*!*********************************************!*\
  !*** ./lib/jupyterlab/local-drive/drive.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DRIVE_NAME": () => (/* binding */ DRIVE_NAME),
/* harmony export */   "FileSystemDrive": () => (/* binding */ FileSystemDrive)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);



const DRIVE_NAME = 'FileSystem';
const DRIVE_PREFIX = `${DRIVE_NAME}:`;
function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}
function base64DecodeAsBlob(text, type = 'text/plain;charset=UTF-8') {
    return fetch(`data:${type};base64,` + text).then(response => response.blob());
}
async function toArray(asyncIterator) {
    const arr = [];
    for await (const i of asyncIterator) {
        arr.push(i);
    }
    return arr;
}
class FileSystemDrive {
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    get name() {
        return DRIVE_NAME;
    }
    get serverSettings() {
        return _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
    }
    get fileChanged() {
        return this._fileChanged;
    }
    get rootHandle() {
        return this._rootHandle;
    }
    set rootHandle(handle) {
        this._rootHandle = handle;
    }
    async get(path, options) {
        path = this.cleanPath(path);
        const root = this._rootHandle;
        if (!root) {
            return {
                name: '',
                path: '',
                created: new Date().toISOString(),
                last_modified: new Date().toISOString(),
                format: null,
                mimetype: '',
                content: null,
                writable: true,
                type: 'directory'
            };
        }
        const parentHandle = await this.getParentHandle(path);
        const parentPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.dirname(path);
        const localPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(path);
        let localHandle;
        if (localPath) {
            localHandle = await this.getHandle(parentHandle, localPath);
        }
        else {
            localHandle = parentHandle;
        }
        if (localHandle.kind === 'file') {
            return this.getFileModel(localHandle, parentPath, true);
        }
        else {
            const content = [];
            for await (const value of localHandle.values()) {
                if (value.kind === 'file') {
                    content.push(await this.getFileModel(value, _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(parentPath, localPath)));
                }
                else {
                    content.push({
                        name: value.name,
                        path: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(parentPath, localPath, value.name),
                        created: '',
                        last_modified: '',
                        format: null,
                        mimetype: '',
                        content: null,
                        writable: true,
                        type: 'directory'
                    });
                }
            }
            return {
                name: localPath,
                path: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(parentPath, localPath),
                last_modified: '',
                created: '',
                format: null,
                mimetype: '',
                content,
                size: undefined,
                writable: true,
                type: 'directory'
            };
        }
    }
    async getDownloadUrl(path) {
        throw new Error('Method not implemented.');
    }
    async newUntitled(options) {
        let parentPath = '';
        if (options && options.path) {
            parentPath = this.cleanPath(options.path);
        }
        const type = options?.type || 'directory';
        const path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(parentPath, type === 'directory' ? 'Untitled Folder' : 'untitled');
        const ext = options?.ext || 'txt';
        const parentHandle = await this.getParentHandle(path);
        let localPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(path);
        const name = localPath;
        let data;
        if (type === 'directory') {
            let i = 1;
            while (await this.hasHandle(parentHandle, localPath)) {
                localPath = `${name} ${i++}`;
            }
            await parentHandle.getDirectoryHandle(localPath, { create: true });
            data = await this.get(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(parentPath, localPath));
        }
        else {
            let i = 1;
            while (await this.hasHandle(parentHandle, `${localPath}.${ext}`)) {
                localPath = `${name}${i++}`;
            }
            const filename = `${localPath}.${ext}`;
            await parentHandle.getFileHandle(filename, { create: true });
            data = await this.get(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(parentPath, filename));
        }
        this._fileChanged.emit({
            type: 'new',
            oldValue: null,
            newValue: data
        });
        return data;
    }
    async delete(path) {
        path = this.cleanPath(path);
        const parentHandle = await this.getParentHandle(path);
        await parentHandle.removeEntry(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(path), { recursive: true });
        this._fileChanged.emit({
            type: 'delete',
            oldValue: { path: path },
            newValue: null
        });
    }
    async rename(oldPath, newPath) {
        // Best effort, we are lacking proper APIs for renaming
        oldPath = this.cleanPath(oldPath);
        newPath = this.cleanPath(newPath);
        await this.doCopy(oldPath, newPath);
        await this.delete(oldPath);
        const data = this.get(newPath);
        data.then(model => {
            this._fileChanged.emit({
                type: 'rename',
                oldValue: { path: oldPath },
                newValue: model
            });
        });
        return data;
    }
    async save(path, options) {
        path = this.cleanPath(path);
        const parentHandle = await this.getParentHandle(path);
        if (options?.type === 'directory') {
            await parentHandle.getDirectoryHandle(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(path), {
                create: true
            });
            return this.get(path);
        }
        const handle = await parentHandle.getFileHandle(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(path), {
            create: true
        });
        const writable = await handle.createWritable({});
        const format = options?.format;
        const content = options?.content;
        if (format === 'json') {
            const data = JSON.stringify(content, null, 2);
            await writable.write(data);
        }
        else if (format === 'base64') {
            const contentBlob = await base64DecodeAsBlob(content);
            await writable.write(contentBlob);
        }
        else {
            await writable.write(content);
        }
        await writable.close();
        return this.get(path);
    }
    async copy(path, toLocalDir) {
        // Best effort, we are lacking proper APIs for copying
        path = this.cleanPath(path);
        const toCopy = await this.get(path);
        const parentPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.dirname(path);
        let newName = toCopy.name;
        if (parentPath === toLocalDir) {
            const ext = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.extname(toCopy.name);
            if (ext) {
                newName = `${newName.slice(0, newName.length - ext.length)} (Copy)${ext}`;
            }
            else {
                newName = `${newName} (Copy)`;
            }
        }
        const newPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(toLocalDir, newName);
        await this.doCopy(path, newPath);
        return this.get(newPath);
    }
    async createCheckpoint(path) {
        return {
            id: 'test',
            last_modified: new Date().toISOString()
        };
    }
    async listCheckpoints(path) {
        return [
            {
                id: 'test',
                last_modified: new Date().toISOString()
            }
        ];
    }
    restoreCheckpoint(path, checkpointID) {
        return Promise.resolve(void 0);
    }
    deleteCheckpoint(path, checkpointID) {
        return Promise.resolve(void 0);
    }
    async getParentHandle(path) {
        const root = this._rootHandle;
        if (!root) {
            throw new Error('No root file handle');
        }
        let parentHandle = root;
        for (const subPath of path.split('/').slice(0, -1)) {
            parentHandle = await parentHandle.getDirectoryHandle(subPath);
        }
        return parentHandle;
    }
    async getHandle(parentHandle, localPath) {
        const content = await toArray(parentHandle.values());
        const matches = content.filter(element => element.name === localPath);
        if (matches.length) {
            return matches[0];
        }
        throw new Error(`${localPath} does not exist.`);
    }
    async hasHandle(parentHandle, localPath) {
        const content = await toArray(parentHandle.values());
        const matches = content.filter(element => element.name === localPath);
        return Boolean(matches.length);
    }
    async getFileModel(handle, path, content) {
        const file = await handle.getFile();
        let format;
        let fileContent = null;
        // We assume here image, audio and video mimetypes are all and only binary files we'll encounter
        if (file.type &&
            file.type.split('/') &&
            ['image', 'audio', 'video'].includes(file.type.split('/')[0])) {
            format = 'base64';
        }
        else {
            format = 'text';
        }
        if (content) {
            if (format === 'base64') {
                fileContent = arrayBufferToBase64(await file.arrayBuffer());
            }
            else {
                fileContent = await file.text();
            }
        }
        return {
            name: file.name,
            path: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(path, file.name),
            created: new Date(file.lastModified).toISOString(),
            last_modified: new Date(file.lastModified).toISOString(),
            format,
            content: fileContent,
            writable: true,
            type: 'file',
            mimetype: file.type
        };
    }
    async doCopy(oldPath, newPath) {
        // Best effort, we are lacking proper APIs for copying
        const oldParentHandle = await this.getParentHandle(oldPath);
        const oldLocalPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(oldPath);
        let oldHandle;
        if (oldLocalPath) {
            oldHandle = await this.getHandle(oldParentHandle, oldLocalPath);
        }
        else {
            oldHandle = oldParentHandle;
        }
        const newParentHandle = await this.getParentHandle(newPath);
        const newLocalPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(newPath);
        if (oldHandle.kind === 'directory') {
            // If it's a directory, create directory, then doCopy for the directory content
            await newParentHandle.getDirectoryHandle(newLocalPath, { create: true });
            for await (const content of oldHandle.values()) {
                await this.doCopy(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(oldPath, content.name), _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(newPath, content.name));
            }
        }
        else {
            // If it's a file, copy the file content
            const newFileHandle = await newParentHandle.getFileHandle(newLocalPath, {
                create: true
            });
            const writable = await newFileHandle.createWritable({});
            const file = await oldHandle.getFile();
            const data = await file.arrayBuffer();
            writable.write(data);
            await writable.close();
        }
    }
    cleanPath(path) {
        if (path.includes(DRIVE_PREFIX)) {
            return path.replace(DRIVE_PREFIX, '');
        }
        return path;
    }
    _isDisposed = false;
    _fileChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
    _rootHandle = null;
}


/***/ }),

/***/ "./lib/jupyterlab/local-drive/index.js":
/*!*********************************************!*\
  !*** ./lib/jupyterlab/local-drive/index.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _drive__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./drive */ "./lib/jupyterlab/local-drive/drive.js");






/**
 * The file system access factory
 */
const FILE_SYSTEM_ACCESS_FACTORY = 'FileSystemAccess';
/**
 * The class name added to the filebrowser filterbox node.
 */
const FILTERBOX_CLASS = 'jp-FileBrowser-filterBox';
/**
 * Initialization data for the jupyterlab-filesystem-access extension.
 */
const plugin = {
    id: '@datalayer/run:local-drive',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IToolbarWidgetRegistry],
    autoStart: true,
    activate: (app, browser, translator, settingRegistry, toolbarRegistry) => {
        const showDirectoryPicker = window.showDirectoryPicker;
        if (!showDirectoryPicker) {
            // bail if the browser does not support the File System API
            console.warn('The File System Access APII is not supported in this browser.');
            return;
        }
        const { serviceManager } = app;
        const { createFileBrowser } = browser;
        const trans = translator.load('jupyterlab-filesystem-access');
        const drive = new _drive__WEBPACK_IMPORTED_MODULE_5__.FileSystemDrive();
        serviceManager.contents.addDrive(drive);
        const widget = createFileBrowser('jp-filesystem-browser', {
            driveName: drive.name,
            // We don't want to restore old state, we don't have a drive handle ready
            restore: false
        });
        widget.title.caption = trans.__('Local File System');
        widget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.listIcon;
        // set some defaults for now
        widget.showFileCheckboxes = false;
        const toolbar = widget.toolbar;
        toolbar.id = 'jp-filesystem-toolbar';
        if (toolbarRegistry && settingRegistry) {
            // Set toolbar
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.setToolbar)(toolbar, (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.createToolbarFactory)(toolbarRegistry, settingRegistry, FILE_SYSTEM_ACCESS_FACTORY, plugin.id, translator ?? _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator), toolbar);
            toolbarRegistry.addFactory(FILE_SYSTEM_ACCESS_FACTORY, 'open-folder', (browser) => {
                const openDirectoryButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
                    icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.folderIcon,
                    onClick: async () => {
                        const directoryHandle = await showDirectoryPicker();
                        if (directoryHandle) {
                            drive.rootHandle = directoryHandle;
                            // Go to root directory
                            widget.model.cd('/');
                        }
                    },
                    tooltip: trans.__('Open a new folder')
                });
                return openDirectoryButton;
            });
            toolbarRegistry.addFactory(FILE_SYSTEM_ACCESS_FACTORY, 'uploader', (browser) => new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.Uploader({
                model: widget.model,
                translator
            }));
            toolbarRegistry.addFactory(FILE_SYSTEM_ACCESS_FACTORY, 'filename-searcher', (browser) => {
                const searcher = (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.FilenameSearcher)({
                    updateFilter: (filterFn, query) => {
                        widget.model.setFilter(value => {
                            return filterFn(value.name.toLowerCase());
                        });
                    },
                    useFuzzyFilter: true,
                    placeholder: trans.__('Filter files by name'),
                    forceRefresh: false
                });
                searcher.addClass(FILTERBOX_CLASS);
                return searcher;
            });
        }
        app.shell.add(widget, 'left', { type: 'FileSystemAccess' });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/jupyterlab/service/DatalayerServiceManager.js":
/*!***********************************************************!*\
  !*** ./lib/jupyterlab/service/DatalayerServiceManager.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DatalayerServiceManager": () => (/* binding */ DatalayerServiceManager),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
class DatalayerServiceManager {
    _serviceManager;
    constructor(serviceManager) {
        this._serviceManager = serviceManager;
    }
    get isReady() {
        return this._serviceManager.isReady;
    }
    get ready() {
        return this._serviceManager.ready;
    }
    get connectionFailure() {
        return this._serviceManager.connectionFailure;
    }
    get isDisposed() {
        return this._serviceManager.isDisposed;
    }
    get builder() {
        return this._serviceManager.builder;
    }
    get contents() {
        return this._serviceManager.contents;
    }
    get events() {
        return this._serviceManager.events;
    }
    get serverSettings() {
        return this._serviceManager.serverSettings;
    }
    get sessions() {
        return this._serviceManager.sessions;
    }
    get kernels() {
        return this._serviceManager.kernels;
    }
    get kernelspecs() {
        return this._serviceManager.kernelspecs;
    }
    get settings() {
        return this._serviceManager.settings;
    }
    get terminals() {
        return this._serviceManager.terminals;
    }
    get user() {
        return this._serviceManager.user;
    }
    get workspaces() {
        return this._serviceManager.workspaces;
    }
    get nbconvert() {
        return this._serviceManager.nbconvert;
    }
    dispose() {
        this._serviceManager.dispose();
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DatalayerServiceManager);


/***/ }),

/***/ "./lib/jupyterlab/widget.js":
/*!**********************************!*\
  !*** ./lib/jupyterlab/widget.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DatalayerRunWidget": () => (/* binding */ DatalayerRunWidget)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @datalayer/jupyter-react */ "webpack/sharing/consume/default/@datalayer/jupyter-react/@datalayer/jupyter-react");
/* harmony import */ var _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _Run__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../Run */ "./lib/Run.js");




class DatalayerRunWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    _app;
    //  private _jupyterRun: IDatalayerRun;
    constructor(app, jupyterRun) {
        super();
        this._app = app;
        //    this._jupyterRun = jupyterRun;
        this.addClass('dla-Container');
    }
    render() {
        return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_Run__WEBPACK_IMPORTED_MODULE_3__["default"], { adapter: _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_2__.JupyterLabAppAdapter.create(this._app) }) }));
    }
}


/***/ }),

/***/ "./lib/state/mobx.js":
/*!***************************!*\
  !*** ./lib/state/mobx.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MobxTimer": () => (/* binding */ MobxTimer),
/* harmony export */   "MobxTimerView": () => (/* binding */ MobxTimerView),
/* harmony export */   "mobxTimer": () => (/* binding */ mobxTimer)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var mobx__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! mobx */ "webpack/sharing/consume/default/mobx/mobx?346a");
/* harmony import */ var mobx__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(mobx__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var mobx_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! mobx-react */ "webpack/sharing/consume/default/mobx-react/mobx-react");
/* harmony import */ var mobx_react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(mobx_react__WEBPACK_IMPORTED_MODULE_2__);



class MobxTimer {
    secondsPassed = 0;
    constructor() {
        (0,mobx__WEBPACK_IMPORTED_MODULE_1__.makeAutoObservable)(this);
    }
    reset() {
        this.secondsPassed = 0;
    }
    increaseTimer() {
        this.secondsPassed += 1;
    }
}
const mobxTimer = new MobxTimer();
setInterval(() => {
    mobxTimer.increaseTimer();
}, 1000);
const MobxTimerView = (0,mobx_react__WEBPACK_IMPORTED_MODULE_2__.observer)(({ mobxTimer }) => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("button", { onClick: () => mobxTimer.reset(), children: ["Datalayer Run Mobx: ", mobxTimer.secondsPassed] })));


/***/ }),

/***/ "./lib/state/zustand.js":
/*!******************************!*\
  !*** ./lib/state/zustand.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Timer": () => (/* binding */ Timer),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "useStore": () => (/* binding */ useStore)
/* harmony export */ });
/* harmony import */ var zustand__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! zustand */ "webpack/sharing/consume/default/zustand/zustand");
/* harmony import */ var zustand__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(zustand__WEBPACK_IMPORTED_MODULE_0__);

class Timer {
    _secondsPassed = 0;
    constructor() {
    }
    reset() {
        this._secondsPassed = 0;
    }
    increaseTimer() {
        this._secondsPassed += 1;
    }
    get secondsPassed() {
        return this._secondsPassed;
    }
}
const useStore = (0,zustand__WEBPACK_IMPORTED_MODULE_0__.create)((set, get) => ({
    tab: 0.0,
    getIntTab: () => Math.floor(get().tab),
    setTab: (tab) => set((state) => ({ tab })),
    timer: new Timer(),
    increaseTimer: () => {
        get().timer.increaseTimer();
        set((state) => ({ secondsPassed: get().timer.secondsPassed }));
    },
    secondsPassed: 0,
}));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (useStore);


/***/ }),

/***/ "./lib/tabs/AboutTab.js":
/*!******************************!*\
  !*** ./lib/tabs/AboutTab.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AboutTab": () => (/* binding */ AboutTab),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Pagehead/Pagehead.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Label/Label.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Link/Link.js");
/* harmony import */ var _datalayer_icons_react_eggs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @datalayer/icons-react/eggs */ "../icons/react/eggs/esm/ECharlesIcon.js");




const AboutTab = (props) => {
    const { version } = props;
    const [egg, setEgg] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_2__["default"], { as: "h2", children: ["\u039E \uD83C\uDFC3 Datalayer Run", (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { marginLeft: 1 }, children: version })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { children: "Datalayer Run." }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { mt: 3, style: { height: 350 }, children: !egg ?
                    (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("img", { src: "https://assets.datalayer.tech/releases/datalayer-0.2.0-omalley.png", onClick: e => setEgg(true) })
                    :
                        (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_icons_react_eggs__WEBPACK_IMPORTED_MODULE_6__["default"], { size: 300, onClick: e => setEgg(false) }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { href: "https://datalayer.tech/docs/releases/0.2.0-omalley", target: "_blank", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "h4", children: "Datalayer 0.2.0 O'Malley Release" }) }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { href: "https://github.com/datalayer/run", target: "_blank", children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_5__["default"], { as: "h4", children: "Source code" }) }) })] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (AboutTab);


/***/ }),

/***/ "./lib/tabs/ContainersTab.js":
/*!***********************************!*\
  !*** ./lib/tabs/ContainersTab.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Button/IconButton.js");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @primer/octicons-react */ "../../../node_modules/@primer/octicons-react/dist/index.esm.js");
/* harmony import */ var _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @datalayer/icons-react */ "../icons/react/data1/esm/TerminalIcon.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/index.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/DataTable.js");
/* harmony import */ var _jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../jupyterlab/handler */ "./lib/jupyterlab/handler.js");







const Containers = () => {
    const [containers, setContainers] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    const refreshContainers = () => {
        (0,_jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('containers')
            .then(data => {
            const containers = data.containers.map((container, id) => {
                return {
                    id: container.Id,
                    ...container,
                };
            });
            setContainers(containers);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
    };
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        refreshContainers();
    }, []);
    const terminateContainer = (containerId) => {
        (0,_jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)(`containers/${containerId}`, {
            method: 'DELETE',
        })
            .then(data => {
            console.log('---', data);
            refreshContainers();
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Container, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Title, { as: "h2", id: "containers", children: "Run containers" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Subtitle, { as: "p", id: "containers-subtitle", children: "List of Run containers." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.DataTable, { "aria-labelledby": "containers", "aria-describedby": "containers-subtitle", data: containers, columns: [
                            {
                                header: 'Image',
                                field: 'Config.Image',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Config.Image })
                            },
                            {
                                header: 'Id',
                                field: 'id',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.id })
                            },
                            {
                                header: 'Created',
                                field: 'Created',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Created })
                            },
                            {
                                header: 'Attach',
                                field: 'id',
                                renderCell: row => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__.IconButton, { "aria-label": `Attach to container ID ${row.id}`, icon: _datalayer_icons_react__WEBPACK_IMPORTED_MODULE_8__["default"], size: "small", onClick: () => terminateContainer(row.id) }) }))
                            },
                            {
                                header: 'Terminate',
                                field: 'id',
                                renderCell: row => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__.IconButton, { "aria-label": `Terminate container ID ${row.id}`, icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_9__.XIcon, size: "small", onClick: () => terminateContainer(row.id) }) }))
                            },
                        ] })] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Containers);


/***/ }),

/***/ "./lib/tabs/ImagesTab.js":
/*!*******************************!*\
  !*** ./lib/tabs/ImagesTab.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Button/IconButton.js");
/* harmony import */ var _primer_octicons_react__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @primer/octicons-react */ "../../../node_modules/@primer/octicons-react/dist/index.esm.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/index.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/DataTable.js");
/* harmony import */ var _state_zustand__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../state/zustand */ "./lib/state/zustand.js");
/* harmony import */ var _jupyterlab_handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../jupyterlab/handler */ "./lib/jupyterlab/handler.js");
/* harmony import */ var _utils_Utils__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./../utils/Utils */ "./lib/utils/Utils.js");








const Images = () => {
    const { setTab } = (0,_state_zustand__WEBPACK_IMPORTED_MODULE_2__["default"])();
    const [images, setImages] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_jupyterlab_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('images')
            .then(data => {
            const images = data.images.map((image, id) => {
                return {
                    id,
                    ...image,
                };
            });
            setImages(images.filter(image => image.RepoTags.length > 0));
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
    }, []);
    const startContainer = (imageName) => {
        (0,_jupyterlab_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('containers', {
            method: 'POST',
            body: JSON.stringify({
                imageName,
            })
        })
            .then(data => {
            setTab(1.0);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.Table.Container, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.Table.Title, { as: "h2", id: "images", children: "Run images" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.Table.Subtitle, { as: "p", id: "images-subtitle", children: "List of Run images." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_6__.DataTable, { "aria-labelledby": "images", "aria-describedby": "images-subtitle", data: images, columns: [
                            {
                                header: 'Image Name',
                                field: 'RepoTags',
                                renderCell: row => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: row.RepoTags.map(repoTag => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_4__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { children: (0,_utils_Utils__WEBPACK_IMPORTED_MODULE_8__.strip)(repoTag, 40) }) }))) }))
                            },
                            {
                                header: 'Action',
                                field: 'RepoTags',
                                renderCell: row => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: row.RepoTags.map(repoTag => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_9__.IconButton, { "aria-label": `Start a container with image ${repoTag}`, icon: _primer_octicons_react__WEBPACK_IMPORTED_MODULE_10__.PlayIcon, size: "small", onClick: () => startContainer(repoTag) }))) }))
                            },
                            {
                                header: 'Size',
                                field: 'Size',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { children: row.Size })
                            },
                            {
                                header: 'Os',
                                field: 'Os',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_7__["default"], { children: row.Os })
                            },
                        ] })] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Images);


/***/ }),

/***/ "./lib/tabs/NetworksTab.js":
/*!*********************************!*\
  !*** ./lib/tabs/NetworksTab.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/index.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/DataTable.js");
/* harmony import */ var _jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../jupyterlab/handler */ "./lib/jupyterlab/handler.js");





const Networks = () => {
    const [networks, setNetworks] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('networks')
            .then(data => {
            const networks = data.networks.map((network, id) => {
                return {
                    id: data.Id,
                    ...network,
                };
            });
            setNetworks(networks);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Container, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Title, { as: "h2", id: "networks", children: "Run networks" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Subtitle, { as: "p", id: "networks-subtitle", children: "List of Run networks." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.DataTable, { "aria-labelledby": "networks", "aria-describedby": "networks-subtitle", data: networks, columns: [
                            {
                                header: 'Name',
                                field: 'Name',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Name })
                            },
                            {
                                header: 'Scope',
                                field: 'Scope',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Scope })
                            },
                            {
                                header: 'Ingress',
                                field: 'Ingress',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Ingress })
                            },
                            {
                                header: 'Attachable',
                                field: 'Attachable',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Attachable })
                            },
                        ] })] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Networks);


/***/ }),

/***/ "./lib/tabs/SecretsTab.js":
/*!********************************!*\
  !*** ./lib/tabs/SecretsTab.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/index.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/DataTable.js");
/* harmony import */ var _jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../jupyterlab/handler */ "./lib/jupyterlab/handler.js");





const Secrets = () => {
    const [secrets, setSecrets] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('secrets')
            .then(data => {
            const secrets = data.secrets.map((secret, id) => {
                return {
                    id: secret.ID,
                    ...secret,
                };
            });
            setSecrets(secrets);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Container, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Title, { as: "h2", id: "secrets", children: "Run secrets" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Subtitle, { as: "p", id: "secrets-subtitle", children: "List of Run secrets." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.DataTable, { "aria-labelledby": "secrets", "aria-describedby": "secrets-subtitle", data: secrets, columns: [
                            {
                                header: 'Name',
                                field: 'Spec.Name',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Spec.Name })
                            },
                            {
                                header: 'Version',
                                field: 'Version.Index',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Version.Index })
                            },
                            {
                                header: 'CreatedAt',
                                field: 'CreatedAt',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.CreatedAt })
                            },
                        ] })] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Secrets);


/***/ }),

/***/ "./lib/tabs/VolumesTab.js":
/*!********************************!*\
  !*** ./lib/tabs/VolumesTab.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Text/Text.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/index.js");
/* harmony import */ var _primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @primer/react/drafts */ "../../../node_modules/@primer/react/lib-esm/DataTable/DataTable.js");
/* harmony import */ var _jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../jupyterlab/handler */ "./lib/jupyterlab/handler.js");





const Volumes = () => {
    const [volumes, setVolumes] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(new Array());
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        (0,_jupyterlab_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('volumes')
            .then(data => {
            const volumes = data.volumes.map((volume, id) => {
                return {
                    id,
                    ...volume,
                };
            });
            setVolumes(volumes);
        })
            .catch(reason => {
            console.error(`Error while accessing the jupyter server datalayer_run extension.\n${reason}`);
        });
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_3__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Container, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Title, { as: "h2", id: "volumes", children: "Run volumes" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_4__.Table.Subtitle, { as: "p", id: "volumes-subtitle", children: "List of Run volumes." }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_drafts__WEBPACK_IMPORTED_MODULE_5__.DataTable, { "aria-labelledby": "volumes", "aria-describedby": "volumes-subtitle", data: volumes, columns: [
                            {
                                header: 'Name',
                                field: 'Name',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Name })
                            },
                            {
                                header: 'Mountpoint',
                                field: 'Mountpoint',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Mountpoint })
                            },
                            {
                                header: 'CreatedAt',
                                field: 'CreatedAt',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.CreatedAt })
                            },
                            {
                                header: 'Scope',
                                field: 'Scope',
                                renderCell: row => (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_6__["default"], { children: row.Scope })
                            },
                        ] })] }) }) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Volumes);


/***/ }),

/***/ "./lib/timer/TimerView.js":
/*!********************************!*\
  !*** ./lib/timer/TimerView.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TimerView": () => (/* binding */ TimerView)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _state_zustand__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../state/zustand */ "./lib/state/zustand.js");



const TimerView = () => {
    const { timer, increaseTimer, secondsPassed } = (0,_state_zustand__WEBPACK_IMPORTED_MODULE_2__["default"])();
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        setInterval(() => {
            increaseTimer();
        }, 1000);
    }, []);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)("button", { onClick: () => timer.reset(), children: ["Datalayer Run: ", secondsPassed] }));
};


/***/ }),

/***/ "./lib/utils/Utils.js":
/*!****************************!*\
  !*** ./lib/utils/Utils.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "strip": () => (/* binding */ strip)
/* harmony export */ });
const strip = (s, max) => {
    if (s.length > max) {
        return s.slice(0, max) + '...';
    }
    return s;
};


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../../node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "../icons/react/data1/esm/DatalayerGreenPaddingIcon.svg":
/*!**************************************************************!*\
  !*** ../icons/react/data1/esm/DatalayerGreenPaddingIcon.svg ***!
  \**************************************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" aria-hidden=\"true\" viewBox=\"0 0 72 72\">\n  <path fill=\"#2ecc71\" stroke-width=\"2.9\" d=\"M7 7h58v11.6H7zm0 0\"/>\n  <path fill=\"#1abc9c\" stroke-width=\"2.9\" d=\"M7 30.2h58v11.6H7zm0 0\"/>\n  <path fill=\"#16a085\" stroke-width=\"2.9\" d=\"M7 53.4h58V65H7zm0 0\"/>\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_jupyterlab_index_js.573d2482a1420bb89381.js.map