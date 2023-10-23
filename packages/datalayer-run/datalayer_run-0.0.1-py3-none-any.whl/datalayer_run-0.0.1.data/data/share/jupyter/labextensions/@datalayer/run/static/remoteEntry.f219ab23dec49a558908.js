var _JUPYTERLAB;
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "webpack/container/entry/@datalayer/run":
/*!***********************!*\
  !*** container entry ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var moduleMap = {
	"./index": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_primer_react_lib-esm_Box_Box_js-node_modules_primer_react_lib-esm_Link_L-31e0ea"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_styled-components_styled-components"), __webpack_require__.e("lib_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")))));
	},
	"./extension": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_primer_react_lib-esm_Box_Box_js-node_modules_primer_react_lib-esm_Link_L-31e0ea"), __webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1"), __webpack_require__.e("vendors-node_modules_primer_octicons-react_dist_index_esm_js-node_modules_primer_react_lib-es-90d2bf"), __webpack_require__.e("vendors-node_modules_jupyterlab_ui-components_lib_icon_labicon_js-node_modules_primer_react_l-031f0f"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_styled-components_styled-components"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_application-webpack_sharing_consume_default_jupyte-53ede0"), __webpack_require__.e("lib_jupyterlab_index_js")]).then(() => (() => ((__webpack_require__(/*! ./lib/jupyterlab/index.js */ "./lib/jupyterlab/index.js")))));
	},
	"./style": () => {
		return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1"), __webpack_require__.e("style_index_js")]).then(() => (() => ((__webpack_require__(/*! ./style/index.js */ "./style/index.js")))));
	}
};
var get = (module, getScope) => {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(() => {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = (shareScope, initScope) => {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: () => (get),
	init: () => (init)
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			loaded: false,
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/create fake namespace object */
/******/ 	(() => {
/******/ 		var getProto = Object.getPrototypeOf ? (obj) => (Object.getPrototypeOf(obj)) : (obj) => (obj.__proto__);
/******/ 		var leafPrototypes;
/******/ 		// create a fake namespace object
/******/ 		// mode & 1: value is a module id, require it
/******/ 		// mode & 2: merge all properties of value into the ns
/******/ 		// mode & 4: return value when already ns object
/******/ 		// mode & 16: return value when it's Promise-like
/******/ 		// mode & 8|1: behave like require
/******/ 		__webpack_require__.t = function(value, mode) {
/******/ 			if(mode & 1) value = this(value);
/******/ 			if(mode & 8) return value;
/******/ 			if(typeof value === 'object' && value) {
/******/ 				if((mode & 4) && value.__esModule) return value;
/******/ 				if((mode & 16) && typeof value.then === 'function') return value;
/******/ 			}
/******/ 			var ns = Object.create(null);
/******/ 			__webpack_require__.r(ns);
/******/ 			var def = {};
/******/ 			leafPrototypes = leafPrototypes || [null, getProto({}), getProto([]), getProto(getProto)];
/******/ 			for(var current = mode & 2 && value; typeof current == 'object' && !~leafPrototypes.indexOf(current); current = getProto(current)) {
/******/ 				Object.getOwnPropertyNames(current).forEach((key) => (def[key] = () => (value[key])));
/******/ 			}
/******/ 			def['default'] = () => (value);
/******/ 			__webpack_require__.d(ns, def);
/******/ 			return ns;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	(() => {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = (chunkId) => {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce((promises, key) => {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	(() => {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = (chunkId) => {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"vendors-node_modules_primer_react_lib-esm_Box_Box_js-node_modules_primer_react_lib-esm_Link_L-31e0ea":"dcbedfbc5657d6dccf4b","webpack_sharing_consume_default_react":"83121611ff1ac807e979","webpack_sharing_consume_default_styled-components_styled-components":"1a5884d5ff7a53b6d045","lib_index_js":"4808b5bcd36375e893e0","vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1":"6bb1534e207960bf0488","vendors-node_modules_primer_octicons-react_dist_index_esm_js-node_modules_primer_react_lib-es-90d2bf":"9804a73fdae4736f1e1c","vendors-node_modules_jupyterlab_ui-components_lib_icon_labicon_js-node_modules_primer_react_l-031f0f":"511c353d410f232011f6","webpack_sharing_consume_default_react-dom":"edce4b8f34433aee339f","webpack_sharing_consume_default_jupyterlab_application-webpack_sharing_consume_default_jupyte-53ede0":"00e5869a4f9e862ebe31","lib_jupyterlab_index_js":"573d2482a1420bb89381","style_index_js":"b4865c412ecd282a29b6","vendors-node_modules_use-sync-external-store_shim_with-selector_js":"be001d9da324cda97bda","vendors-node_modules_codemirror_lang-python_dist_index_js-node_modules_datalayer_typescript-f-d98328":"bfb260e3eff99f64b513","webpack_sharing_consume_default_react-is_react-is-_09cc":"69114d231bbc73ac600e","jupyter_ui_packages_react_lib_index_js-webpack_sharing_consume_default_codemirror_language-we-5dc5b7":"e31b58ebebab9922fb90","vendors-node_modules_mobx-react_dist_mobxreact_esm_js":"5c9c1e30ad253caa5519","webpack_sharing_consume_default_mobx_mobx":"53746537083cd6061ba4","vendors-node_modules_mobx_dist_mobx_esm_js":"d08eb66f4dbf9d0f929c","node_modules_hoist-non-react-statics_node_modules_react-is_index_js":"1f3d090ed8b0b114bcb5","node_modules_react-is_index_js":"b9ae890914c6d4096b25","vendors-node_modules_styled-components_dist_styled-components_browser_esm_js":"fdea8429129680647812","webpack_sharing_consume_default_react-is_react-is-_78ad":"44f0fa47c0914de0caa8","node_modules_zustand_esm_index_mjs-_23790":"e8c98be96a44efd73470","node_modules_zustand_esm_index_mjs-_23791":"834e843088ec2aaa516e","vendors-node_modules_jupyterlab_terminal_style_index_css":"0d73f1f5238d3fca0624","vendors-node_modules_jupyterlab_theme-light-extension_style_theme_css":"8d081e13ec0a4cc0f35c","vendors-node_modules_jupyterlab_theme-dark-extension_style_theme_css":"11597e13d2a31c928d88","node_modules_jupyter-widgets_base_css_index_css":"abe939fb98acd664297f","jupyter_ui_packages_lite_ipykernel-extension_lib_index_js":"73ad5e5ec0e96d18b0fd","vendors-node_modules_async-mutex_index_mjs-node_modules_jupyterlab_services_lib_kernel_serial-bcf9d7":"9e98423f70bd6d0871fc","jupyter_ui_packages_lite_server-extension_lib_index_js":"0b4830485d1333eae191","vendors-node_modules_codemirror_lang-markdown_dist_index_js":"4850ff5c6c5f86c03836","webpack_sharing_consume_default_jupyterlab_application-extension":"4de5e0b6c7d0b7612c38","webpack_sharing_consume_default_jupyterlab_apputils-extension":"73cefa7a67731dc4ddbb","webpack_sharing_consume_default_jupyterlab_codemirror-extension":"8f007c88421d5a5adfba","webpack_sharing_consume_default_jupyterlab_cell-toolbar-extension":"d36bd2a327953a516962","webpack_sharing_consume_default_jupyterlab_completer-extension":"8c78d0fb4515271c4409","webpack_sharing_consume_default_jupyterlab_console-extension":"6290919bc7f34c8939ff","webpack_sharing_consume_default_jupyterlab_docmanager-extension":"e6b641acd16a0fb3443c","webpack_sharing_consume_default_jupyterlab_filebrowser-extension":"9d92ec19b3f4e53cf2d0","webpack_sharing_consume_default_jupyterlab_mainmenu-extension":"df17a110e22684cd9959","webpack_sharing_consume_default_jupyterlab_markdownviewer-extension":"a4d62a643ab958a9f0e9","webpack_sharing_consume_default_jupyterlab_markedparser-extension":"e4cb6724bc453c8492c3","webpack_sharing_consume_default_jupyterlab_fileeditor-extension":"1f8a86d04f2a08a5fa6d","webpack_sharing_consume_default_jupyterlab_launcher-extension":"226ab4b9eba7ccb339b9","webpack_sharing_consume_default_jupyterlab_notebook-extension":"461575c73d6808ae77a0","webpack_sharing_consume_default_jupyterlab_rendermime-extension":"f4828e66474acb676c1e","webpack_sharing_consume_default_jupyterlab_shortcuts-extension":"14a644fb34b2f5e79c2d","webpack_sharing_consume_default_jupyterlab_statusbar-extension":"81e22936cc8891365332","webpack_sharing_consume_default_jupyterlab_translation-extension":"1c8eeab3818c27c752a3","webpack_sharing_consume_default_jupyterlab_ui-components-extension":"73c4b34267e29976b252","webpack_sharing_consume_default_jupyterlab_documentsearch-extension":"297ce1ca9daca8d43291","webpack_sharing_consume_default_jupyterlab_toc-extension":"9b232cd3abdb318983dc","vendors-node_modules_plotly_js_lib_index_js":"88e098de1f18b94f2c75","vendors-node_modules_comlink_dist_esm_comlink_mjs":"4efe2b8e52732fec3f6f","jupyter_ui_packages_lite_ipykernel_lib_worker_js":"b416443d66a2168d0ea2","jupyter_ui_packages_lite_ipykernel_lib_index_js":"97c8ffb7880be2f2f5f0","jupyter_ui_packages_lite_ipykernel_lib_comlink_worker_js":"a1bf567c75a980aca8fc"}[chunkId] + ".js";
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	(() => {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "@datalayer/run:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = (url, done, key, chunkId) => {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = (prev, event) => {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach((fn) => (fn(event)));
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			;
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/node module decorator */
/******/ 	(() => {
/******/ 		__webpack_require__.nmd = (module) => {
/******/ 			module.paths = [];
/******/ 			if (!module.children) module.children = [];
/******/ 			return module;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	(() => {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = (name, initScope) => {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = (msg) => (typeof console !== "undefined" && console.warn && console.warn(msg));
/******/ 			var uniqueName = "@datalayer/run";
/******/ 			var register = (name, version, factory, eager) => {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = (id) => {
/******/ 				var handleError = (err) => (warn("Initialization of sharing external failed: " + err));
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = (module) => (module && module.init && module.init(__webpack_require__.S[name], initScope))
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("@datalayer/jupyter-react", "0.7.14", () => (Promise.all([__webpack_require__.e("vendors-node_modules_use-sync-external-store_shim_with-selector_js"), __webpack_require__.e("vendors-node_modules_primer_react_lib-esm_Box_Box_js-node_modules_primer_react_lib-esm_Link_L-31e0ea"), __webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_css-loader_dist_runtime_cssW-72eba1"), __webpack_require__.e("vendors-node_modules_codemirror_lang-python_dist_index_js-node_modules_datalayer_typescript-f-d98328"), __webpack_require__.e("vendors-node_modules_primer_octicons-react_dist_index_esm_js-node_modules_primer_react_lib-es-90d2bf"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-is_react-is-_09cc"), __webpack_require__.e("webpack_sharing_consume_default_styled-components_styled-components"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("jupyter_ui_packages_react_lib_index_js-webpack_sharing_consume_default_codemirror_language-we-5dc5b7"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_application-webpack_sharing_consume_default_jupyte-53ede0")]).then(() => (() => (__webpack_require__(/*! ../../jupyter/ui/packages/react/lib/index.js */ "../../jupyter/ui/packages/react/lib/index.js"))))));
/******/ 					register("@datalayer/run", "0.0.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_primer_react_lib-esm_Box_Box_js-node_modules_primer_react_lib-esm_Link_L-31e0ea"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_styled-components_styled-components"), __webpack_require__.e("lib_index_js")]).then(() => (() => (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js"))))));
/******/ 					register("mobx-react", "9.0.0", () => (Promise.all([__webpack_require__.e("vendors-node_modules_mobx-react_dist_mobxreact_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_mobx_mobx")]).then(() => (() => (__webpack_require__(/*! ../../../node_modules/mobx-react/dist/mobxreact.esm.js */ "../../../node_modules/mobx-react/dist/mobxreact.esm.js"))))));
/******/ 					register("mobx", "6.10.0", () => (__webpack_require__.e("vendors-node_modules_mobx_dist_mobx_esm_js").then(() => (() => (__webpack_require__(/*! ../../../node_modules/mobx/dist/mobx.esm.js */ "../../../node_modules/mobx/dist/mobx.esm.js"))))));
/******/ 					register("react-is", "16.13.1", () => (__webpack_require__.e("node_modules_hoist-non-react-statics_node_modules_react-is_index_js").then(() => (() => (__webpack_require__(/*! ../../../node_modules/hoist-non-react-statics/node_modules/react-is/index.js */ "../../../node_modules/hoist-non-react-statics/node_modules/react-is/index.js"))))));
/******/ 					register("react-is", "18.2.0", () => (__webpack_require__.e("node_modules_react-is_index_js").then(() => (() => (__webpack_require__(/*! ../../../node_modules/react-is/index.js */ "../../../node_modules/react-is/index.js"))))));
/******/ 					register("styled-components", "5.3.10", () => (Promise.all([__webpack_require__.e("vendors-node_modules_styled-components_dist_styled-components_browser_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-is_react-is-_09cc"), __webpack_require__.e("webpack_sharing_consume_default_react-is_react-is-_78ad")]).then(() => (() => (__webpack_require__(/*! ../../../node_modules/styled-components/dist/styled-components.browser.esm.js */ "../../../node_modules/styled-components/dist/styled-components.browser.esm.js"))))));
/******/ 					register("zustand", "4.4.1", () => (Promise.all([__webpack_require__.e("vendors-node_modules_use-sync-external-store_shim_with-selector_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("node_modules_zustand_esm_index_mjs-_23790")]).then(() => (() => (__webpack_require__(/*! ../../../node_modules/zustand/esm/index.mjs */ "../../../node_modules/zustand/esm/index.mjs"))))));
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(() => (initPromises[name] = 1));
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) scriptUrl = scripts[scripts.length - 1].src
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	(() => {
/******/ 		var parseVersion = (str) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=p=>{return p.split(".").map((p=>{return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = (a, b) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = (range) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = (range, version) => {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var ensureExistence = (scopeName, key) => {
/******/ 			var scope = __webpack_require__.S[scopeName];
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) throw new Error("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 			return scope;
/******/ 		};
/******/ 		var findVersion = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = (scope, key) => {
/******/ 			var versions = scope[key];
/******/ 			return Object.keys(versions).reduce((a, b) => {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = (scope, key, version, requiredVersion) => {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getSingleton = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) typeof console !== "undefined" && console.warn && console.warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getStrictSingletonVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) throw new Error(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var findValidVersion = (scope, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce((a, b) => {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var getInvalidVersionMessage = (scope, scopeName, key, requiredVersion) => {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ") of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map((key) => {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var getValidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			var entry = findValidVersion(scope, key, requiredVersion);
/******/ 			if(entry) return get(entry);
/******/ 			throw new Error(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var warnInvalidVersion = (scope, scopeName, key, requiredVersion) => {
/******/ 			typeof console !== "undefined" && console.warn && console.warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var get = (entry) => {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var init = (fn) => (function(scopeName, a, b, c) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then) return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], a, b, c));
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], a, b, c);
/******/ 		});
/******/ 		
/******/ 		var load = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findVersion(scope, key));
/******/ 		});
/******/ 		var loadFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			return scope && __webpack_require__.o(scope, key) ? get(findVersion(scope, key)) : fallback();
/******/ 		});
/******/ 		var loadVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init((scopeName, scope, key) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getValidVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheck = /*#__PURE__*/ init((scopeName, scope, key, version) => {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonFallback = /*#__PURE__*/ init((scopeName, scope, key, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			var entry = scope && __webpack_require__.o(scope, key) && findValidVersion(scope, key, version);
/******/ 			return entry ? get(entry) : fallback();
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheckFallback = /*#__PURE__*/ init((scopeName, scope, key, version, fallback) => {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/react": () => (loadSingletonVersionCheck("default", "react", [1,18,2,0])),
/******/ 			"webpack/sharing/consume/default/styled-components/styled-components": () => (loadStrictVersionCheckFallback("default", "styled-components", [,[1,5],[1,4],1], () => (Promise.all([__webpack_require__.e("vendors-node_modules_styled-components_dist_styled-components_browser_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_react-is_react-is-_09cc"), __webpack_require__.e("webpack_sharing_consume_default_react-is_react-is-_78ad")]).then(() => (() => (__webpack_require__(/*! styled-components */ "../../../node_modules/styled-components/dist/styled-components.browser.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-dom": () => (loadSingletonVersionCheck("default", "react-dom", [1,18,2,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/coreutils": () => (loadSingletonVersionCheck("default", "@jupyterlab/coreutils", [1,6,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/services": () => (loadSingletonVersionCheck("default", "@jupyterlab/services", [1,7,0,3])),
/******/ 			"webpack/sharing/consume/default/@lumino/coreutils": () => (loadSingletonVersionCheck("default", "@lumino/coreutils", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/signaling": () => (loadSingletonVersionCheck("default", "@lumino/signaling", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/apputils": () => (loadSingletonVersionCheck("default", "@jupyterlab/apputils", [1,4,1,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/translation": () => (loadSingletonVersionCheck("default", "@jupyterlab/translation", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/ui-components": () => (loadSingletonVersionCheck("default", "@jupyterlab/ui-components", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/application": () => (loadSingletonVersionCheck("default", "@jupyterlab/application", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/filebrowser": () => (loadSingletonVersionCheck("default", "@jupyterlab/filebrowser", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/settingregistry": () => (loadSingletonVersionCheck("default", "@jupyterlab/settingregistry", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/launcher": () => (loadSingletonVersionCheck("default", "@jupyterlab/launcher", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/zustand/zustand": () => (loadStrictVersionCheckFallback("default", "zustand", [4,4,4,1], () => (Promise.all([__webpack_require__.e("vendors-node_modules_use-sync-external-store_shim_with-selector_js"), __webpack_require__.e("node_modules_zustand_esm_index_mjs-_23791")]).then(() => (() => (__webpack_require__(/*! zustand */ "../../../node_modules/zustand/esm/index.mjs"))))))),
/******/ 			"webpack/sharing/consume/default/mobx/mobx?346a": () => (loadStrictVersionCheckFallback("default", "mobx", [4,6,10,0], () => (__webpack_require__.e("vendors-node_modules_mobx_dist_mobx_esm_js").then(() => (() => (__webpack_require__(/*! mobx */ "../../../node_modules/mobx/dist/mobx.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/mobx-react/mobx-react": () => (loadStrictVersionCheckFallback("default", "mobx-react", [4,9,0,0], () => (Promise.all([__webpack_require__.e("vendors-node_modules_mobx-react_dist_mobxreact_esm_js"), __webpack_require__.e("webpack_sharing_consume_default_mobx_mobx")]).then(() => (() => (__webpack_require__(/*! mobx-react */ "../../../node_modules/mobx-react/dist/mobxreact.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/@datalayer/jupyter-react/@datalayer/jupyter-react": () => (loadStrictVersionCheckFallback("default", "@datalayer/jupyter-react", [4,0,7,14], () => (Promise.all([__webpack_require__.e("vendors-node_modules_use-sync-external-store_shim_with-selector_js"), __webpack_require__.e("vendors-node_modules_codemirror_lang-python_dist_index_js-node_modules_datalayer_typescript-f-d98328"), __webpack_require__.e("webpack_sharing_consume_default_react-is_react-is-_09cc"), __webpack_require__.e("jupyter_ui_packages_react_lib_index_js-webpack_sharing_consume_default_codemirror_language-we-5dc5b7")]).then(() => (() => (__webpack_require__(/*! @datalayer/jupyter-react */ "../../jupyter/ui/packages/react/lib/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-is/react-is?09cc": () => (loadStrictVersionCheckFallback("default", "react-is", [1,16,7,0], () => (__webpack_require__.e("node_modules_hoist-non-react-statics_node_modules_react-is_index_js").then(() => (() => (__webpack_require__(/*! react-is */ "../../../node_modules/hoist-non-react-statics/node_modules/react-is/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-is/react-is?43d8": () => (loadStrictVersionCheckFallback("default", "react-is", [1,18,0,0], () => (__webpack_require__.e("node_modules_react-is_index_js").then(() => (() => (__webpack_require__(/*! react-is */ "../../../node_modules/react-is/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@lumino/application": () => (loadSingletonVersionCheck("default", "@lumino/application", [1,2,0,1])),
/******/ 			"webpack/sharing/consume/default/@lumino/algorithm": () => (loadSingletonVersionCheck("default", "@lumino/algorithm", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/widgets": () => (loadSingletonVersionCheck("default", "@lumino/widgets", [1,2,0,1])),
/******/ 			"webpack/sharing/consume/default/@lumino/messaging": () => (loadSingletonVersionCheck("default", "@lumino/messaging", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/notebook": () => (loadSingletonVersionCheck("default", "@jupyterlab/notebook", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/documentsearch": () => (loadSingletonVersionCheck("default", "@jupyterlab/documentsearch", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/cells": () => (loadVersionCheck("default", "@jupyterlab/cells", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@lumino/commands": () => (loadSingletonVersionCheck("default", "@lumino/commands", [1,2,0,1])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/codemirror": () => (loadSingletonVersionCheck("default", "@jupyterlab/codemirror", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/completer": () => (loadSingletonVersionCheck("default", "@jupyterlab/completer", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/rendermime": () => (loadSingletonVersionCheck("default", "@jupyterlab/rendermime", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyter/ydoc": () => (loadSingletonVersionCheck("default", "@jupyter/ydoc", [1,1,0,2])),
/******/ 			"webpack/sharing/consume/default/@lumino/domutils": () => (loadSingletonVersionCheck("default", "@lumino/domutils", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/outputarea": () => (loadVersionCheck("default", "@jupyterlab/outputarea", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@codemirror/state": () => (loadSingletonVersionCheck("default", "@codemirror/state", [1,6,2,0])),
/******/ 			"webpack/sharing/consume/default/@codemirror/view": () => (loadSingletonVersionCheck("default", "@codemirror/view", [1,6,9,6])),
/******/ 			"webpack/sharing/consume/default/@codemirror/language": () => (loadSingletonVersionCheck("default", "@codemirror/language", [1,6,0,0])),
/******/ 			"webpack/sharing/consume/default/@lezer/common": () => (loadSingletonVersionCheck("default", "@lezer/common", [1,1,0,0])),
/******/ 			"webpack/sharing/consume/default/@lezer/highlight": () => (loadSingletonVersionCheck("default", "@lezer/highlight", [1,1,0,0])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docregistry": () => (loadVersionCheck("default", "@jupyterlab/docregistry", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/json-extension": () => (loadVersionCheck("default", "@jupyterlab/json-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/javascript-extension": () => (loadVersionCheck("default", "@jupyterlab/javascript-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/mathjax-extension": () => (loadVersionCheck("default", "@jupyterlab/mathjax-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@lumino/disposable": () => (loadSingletonVersionCheck("default", "@lumino/disposable", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/@lumino/properties": () => (loadSingletonVersionCheck("default", "@lumino/properties", [1,2,0,0])),
/******/ 			"webpack/sharing/consume/default/react-is/react-is?882a": () => (loadStrictVersionCheckFallback("default", "react-is", [1,18,2,0], () => (__webpack_require__.e("node_modules_react-is_index_js").then(() => (() => (__webpack_require__(/*! react-is */ "../../../node_modules/react-is/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/console": () => (loadSingletonVersionCheck("default", "@jupyterlab/console", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docmanager": () => (loadSingletonVersionCheck("default", "@jupyterlab/docmanager", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/fileeditor": () => (loadSingletonVersionCheck("default", "@jupyterlab/fileeditor", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/terminal": () => (loadSingletonVersionCheck("default", "@jupyterlab/terminal", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/mobx/mobx?d57d": () => (loadStrictVersionCheckFallback("default", "mobx", [1,6,9,0], () => (__webpack_require__.e("vendors-node_modules_mobx_dist_mobx_esm_js").then(() => (() => (__webpack_require__(/*! mobx */ "../../../node_modules/mobx/dist/mobx.esm.js"))))))),
/******/ 			"webpack/sharing/consume/default/react-is/react-is?78ad": () => (loadStrictVersionCheckFallback("default", "react-is", [0,16,8,0], () => (__webpack_require__.e("node_modules_react-is_index_js").then(() => (() => (__webpack_require__(/*! react-is */ "../../../node_modules/react-is/index.js"))))))),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/observables": () => (loadVersionCheck("default", "@jupyterlab/observables", [1,5,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/application-extension": () => (loadVersionCheck("default", "@jupyterlab/application-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/apputils-extension": () => (loadVersionCheck("default", "@jupyterlab/apputils-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/codemirror-extension": () => (loadVersionCheck("default", "@jupyterlab/codemirror-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/cell-toolbar-extension": () => (loadVersionCheck("default", "@jupyterlab/cell-toolbar-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/completer-extension": () => (loadVersionCheck("default", "@jupyterlab/completer-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/console-extension": () => (loadVersionCheck("default", "@jupyterlab/console-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docmanager-extension": () => (loadVersionCheck("default", "@jupyterlab/docmanager-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/filebrowser-extension": () => (loadVersionCheck("default", "@jupyterlab/filebrowser-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/mainmenu-extension": () => (loadVersionCheck("default", "@jupyterlab/mainmenu-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/markdownviewer-extension": () => (loadVersionCheck("default", "@jupyterlab/markdownviewer-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/markedparser-extension": () => (loadVersionCheck("default", "@jupyterlab/markedparser-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/fileeditor-extension": () => (loadVersionCheck("default", "@jupyterlab/fileeditor-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/launcher-extension": () => (loadVersionCheck("default", "@jupyterlab/launcher-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/notebook-extension": () => (loadVersionCheck("default", "@jupyterlab/notebook-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/rendermime-extension": () => (loadVersionCheck("default", "@jupyterlab/rendermime-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/shortcuts-extension": () => (loadVersionCheck("default", "@jupyterlab/shortcuts-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/statusbar-extension": () => (loadVersionCheck("default", "@jupyterlab/statusbar-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/translation-extension": () => (loadVersionCheck("default", "@jupyterlab/translation-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/ui-components-extension": () => (loadVersionCheck("default", "@jupyterlab/ui-components-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/documentsearch-extension": () => (loadVersionCheck("default", "@jupyterlab/documentsearch-extension", [1,4,0,3])),
/******/ 			"webpack/sharing/consume/default/@jupyterlab/toc-extension": () => (loadVersionCheck("default", "@jupyterlab/toc-extension", [1,6,0,3]))
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_react": [
/******/ 				"webpack/sharing/consume/default/react"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_styled-components_styled-components": [
/******/ 				"webpack/sharing/consume/default/styled-components/styled-components"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-dom": [
/******/ 				"webpack/sharing/consume/default/react-dom"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_application-webpack_sharing_consume_default_jupyte-53ede0": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/coreutils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/services",
/******/ 				"webpack/sharing/consume/default/@lumino/coreutils",
/******/ 				"webpack/sharing/consume/default/@lumino/signaling",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/apputils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/translation",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/ui-components",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/application",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/filebrowser"
/******/ 			],
/******/ 			"lib_jupyterlab_index_js": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/settingregistry",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/launcher",
/******/ 				"webpack/sharing/consume/default/zustand/zustand",
/******/ 				"webpack/sharing/consume/default/mobx/mobx?346a",
/******/ 				"webpack/sharing/consume/default/mobx-react/mobx-react",
/******/ 				"webpack/sharing/consume/default/@datalayer/jupyter-react/@datalayer/jupyter-react"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-is_react-is-_09cc": [
/******/ 				"webpack/sharing/consume/default/react-is/react-is?09cc"
/******/ 			],
/******/ 			"jupyter_ui_packages_react_lib_index_js-webpack_sharing_consume_default_codemirror_language-we-5dc5b7": [
/******/ 				"webpack/sharing/consume/default/react-is/react-is?43d8",
/******/ 				"webpack/sharing/consume/default/@lumino/application",
/******/ 				"webpack/sharing/consume/default/@lumino/algorithm",
/******/ 				"webpack/sharing/consume/default/@lumino/widgets",
/******/ 				"webpack/sharing/consume/default/@lumino/messaging",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/notebook",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/documentsearch",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/cells",
/******/ 				"webpack/sharing/consume/default/@lumino/commands",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/codemirror",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/completer",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/rendermime",
/******/ 				"webpack/sharing/consume/default/@jupyter/ydoc",
/******/ 				"webpack/sharing/consume/default/@lumino/domutils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/outputarea",
/******/ 				"webpack/sharing/consume/default/@codemirror/state",
/******/ 				"webpack/sharing/consume/default/@codemirror/view",
/******/ 				"webpack/sharing/consume/default/@codemirror/language",
/******/ 				"webpack/sharing/consume/default/@lezer/common",
/******/ 				"webpack/sharing/consume/default/@lezer/highlight",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docregistry",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/json-extension",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/javascript-extension",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/mathjax-extension",
/******/ 				"webpack/sharing/consume/default/@lumino/disposable",
/******/ 				"webpack/sharing/consume/default/@lumino/properties",
/******/ 				"webpack/sharing/consume/default/react-is/react-is?882a",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/console",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docmanager",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/fileeditor",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/terminal"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_mobx_mobx": [
/******/ 				"webpack/sharing/consume/default/mobx/mobx?d57d"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-is_react-is-_78ad": [
/******/ 				"webpack/sharing/consume/default/react-is/react-is?78ad"
/******/ 			],
/******/ 			"jupyter_ui_packages_lite_server-extension_lib_index_js": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/observables"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_application-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/application-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_apputils-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/apputils-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_codemirror-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/codemirror-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_cell-toolbar-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/cell-toolbar-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_completer-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/completer-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_console-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/console-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_docmanager-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docmanager-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_filebrowser-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/filebrowser-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_mainmenu-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/mainmenu-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_markdownviewer-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/markdownviewer-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_markedparser-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/markedparser-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_fileeditor-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/fileeditor-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_launcher-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/launcher-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_notebook-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/notebook-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_rendermime-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/rendermime-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_shortcuts-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/shortcuts-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_statusbar-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/statusbar-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_translation-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/translation-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_ui-components-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/ui-components-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_documentsearch-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/documentsearch-extension"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_jupyterlab_toc-extension": [
/******/ 				"webpack/sharing/consume/default/@jupyterlab/toc-extension"
/******/ 			]
/******/ 		};
/******/ 		__webpack_require__.f.consumes = (chunkId, promises) => {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach((id) => {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					var onFactory = (factory) => {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					var onError = (error) => {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = (module) => {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		__webpack_require__.b = document.baseURI || self.location.href;
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"@datalayer/run": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = (chunkId, promises) => {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^webpack_sharing_consume_default_(jupyterlab_(app(lication\-(extension|webpack_sharing_consume_default_jupyte\-53ede0)|utils\-extension)|c(o(demirror|mpleter|nsole)\-extension|ell\-toolbar\-extension)|doc(manager|umentsearch)\-extension|file(browse|edito)r\-extension|ma(rk(downview|edpars)er\-extension|inmenu\-extension)|((shortcu|ui\-componen)ts|launcher|notebook|rendermime|statusbar|toc|translation)\-extension)|react(\-(is_react\-is\-_(09cc|78ad)|dom)|)|mobx_mobx|styled\-components_styled\-components)$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise((resolve, reject) => (installedChunkData = installedChunks[chunkId] = [resolve, reject]));
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = (event) => {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	(() => {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__("webpack/container/entry/@datalayer/run");
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB)["@datalayer/run"] = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.f219ab23dec49a558908.js.map