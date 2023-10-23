"use strict";
(self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || []).push([["lib_index_js"],{

/***/ "../../../node_modules/@primer/react/lib-esm/Label/Label.js":
/*!******************************************************************!*\
  !*** ../../../node_modules/@primer/react/lib-esm/Label/Label.js ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ Label$1),
/* harmony export */   "variants": () => (/* binding */ variants)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! styled-components */ "webpack/sharing/consume/default/styled-components/styled-components");
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(styled_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var styled_system__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! styled-system */ "../../../node_modules/styled-system/dist/index.esm.js");
/* harmony import */ var _constants_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../constants.js */ "../../../node_modules/@primer/react/lib-esm/constants.js");
/* harmony import */ var _sx_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../sx.js */ "../../../node_modules/@primer/react/lib-esm/sx.js");






function _extends() { _extends = Object.assign ? Object.assign.bind() : function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }
const variants = {
  default: {
    borderColor: 'border.default'
  },
  primary: {
    borderColor: 'fg.default'
  },
  secondary: {
    borderColor: 'border.muted',
    color: 'fg.muted'
  },
  accent: {
    borderColor: 'accent.emphasis',
    color: 'accent.fg'
  },
  success: {
    borderColor: 'success.emphasis',
    color: 'success.fg'
  },
  attention: {
    borderColor: 'attention.emphasis',
    color: 'attention.fg'
  },
  severe: {
    borderColor: 'severe.emphasis',
    color: 'severe.fg'
  },
  danger: {
    borderColor: 'danger.emphasis',
    color: 'danger.fg'
  },
  done: {
    borderColor: 'done.emphasis',
    color: 'done.fg'
  },
  sponsors: {
    borderColor: 'sponsors.emphasis',
    color: 'sponsors.fg'
  }
};
const sizes = {
  small: {
    height: '20px',
    padding: '0 7px' // hard-coded to align with Primer ViewComponents and Primer CSS
  },

  large: {
    height: '24px',
    padding: '0 10px' // hard-coded to align with Primer ViewComponents and Primer CSS
  }
};

const StyledLabel = styled_components__WEBPACK_IMPORTED_MODULE_1___default().span.withConfig({
  displayName: "Label__StyledLabel",
  componentId: "sc-1dgcne-0"
})(["align-items:center;background-color:transparent;border-width:1px;border-radius:999px;border-style:solid;display:inline-flex;font-weight:", ";font-size:", ";line-height:1;white-space:nowrap;", ";", ";", ";"], (0,_constants_js__WEBPACK_IMPORTED_MODULE_3__.get)('fontWeights.bold'), (0,_constants_js__WEBPACK_IMPORTED_MODULE_3__.get)('fontSizes.0'), (0,styled_system__WEBPACK_IMPORTED_MODULE_2__.variant)({
  variants
}), (0,styled_system__WEBPACK_IMPORTED_MODULE_2__.variant)({
  prop: 'size',
  variants: sizes
}), _sx_js__WEBPACK_IMPORTED_MODULE_4__["default"]);
const Label = /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default().forwardRef(function Label({
  as,
  size = 'small',
  variant = 'default',
  ...rest
}, ref) {
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default().createElement(StyledLabel, _extends({
    as: as,
    size: size,
    variant: variant,
    ref: ref
  }, rest));
});
var Label$1 = Label;




/***/ }),

/***/ "../../../node_modules/@primer/react/lib-esm/Pagehead/Pagehead.js":
/*!************************************************************************!*\
  !*** ../../../node_modules/@primer/react/lib-esm/Pagehead/Pagehead.js ***!
  \************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ Pagehead$1)
/* harmony export */ });
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! styled-components */ "webpack/sharing/consume/default/styled-components/styled-components");
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(styled_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _constants_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../constants.js */ "../../../node_modules/@primer/react/lib-esm/constants.js");
/* harmony import */ var _sx_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../sx.js */ "../../../node_modules/@primer/react/lib-esm/sx.js");




const Pagehead = styled_components__WEBPACK_IMPORTED_MODULE_0___default().div.withConfig({
  displayName: "Pagehead",
  componentId: "sc-diawfz-0"
})(["position:relative;padding-top:", ";padding-bottom:", ";margin-bottom:", ";border-bottom:1px solid ", ";", ";"], (0,_constants_js__WEBPACK_IMPORTED_MODULE_1__.get)('space.4'), (0,_constants_js__WEBPACK_IMPORTED_MODULE_1__.get)('space.4'), (0,_constants_js__WEBPACK_IMPORTED_MODULE_1__.get)('space.4'), (0,_constants_js__WEBPACK_IMPORTED_MODULE_1__.get)('colors.border.default'), _sx_js__WEBPACK_IMPORTED_MODULE_2__["default"]);
var Pagehead$1 = Pagehead;




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

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AboutTab": () => (/* reexport safe */ _tabs_AboutTab__WEBPACK_IMPORTED_MODULE_0__.AboutTab)
/* harmony export */ });
/* harmony import */ var _tabs_AboutTab__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tabs/AboutTab */ "./lib/tabs/AboutTab.js");



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


/***/ })

}]);
//# sourceMappingURL=lib_index_js.4808b5bcd36375e893e0.js.map