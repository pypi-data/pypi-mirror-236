(()=>{let e;var t,r,n,i,o,s,a=globalThis;function l(e,t){return function(){return e.apply(t,arguments)}}// utils is a library of generic helper functions non-specific to axios
let{toString:u}=Object.prototype,{getPrototypeOf:c}=Object,d=(t=Object.create(null),e=>{let r=u.call(e);return t[r]||(t[r]=r.slice(8,-1).toLowerCase())}),f=e=>(e=e.toLowerCase(),t=>d(t)===e),p=e=>t=>typeof t===e,{isArray:h}=Array,m=p("undefined"),g=f("ArrayBuffer"),y=p("string"),b=p("function"),E=p("number"),w=e=>null!==e&&"object"==typeof e,O=e=>{if("object"!==d(e))return!1;let t=c(e);return(null===t||t===Object.prototype||null===Object.getPrototypeOf(t))&&!(Symbol.toStringTag in e)&&!(Symbol.iterator in e)},S=f("Date"),v=f("File"),R=f("Blob"),A=f("FileList"),T=f("URLSearchParams");/**
 * Iterate over an Array or an Object invoking a function for each item.
 *
 * If `obj` is an Array callback will be called passing
 * the value, index, and complete array for each item.
 *
 * If 'obj' is an Object callback will be called passing
 * the value, key, and complete object for each property.
 *
 * @param {Object|Array} obj The object to iterate
 * @param {Function} fn The callback to invoke for each item
 *
 * @param {Boolean} [allOwnKeys = false]
 * @returns {any}
 */function C(e,t,{allOwnKeys:r=!1}={}){let n,i;// Don't bother if no value provided
if(null!=e){if("object"!=typeof e&&/*eslint no-param-reassign:0*/(e=[e]),h(e))for(n=0,i=e.length;n<i;n++)t.call(null,e[n],n,e);else{let i;// Iterate over object keys
let o=r?Object.getOwnPropertyNames(e):Object.keys(e),s=o.length;for(n=0;n<s;n++)i=o[n],t.call(null,e[i],i,e)}}}function x(e,t){let r;t=t.toLowerCase();let n=Object.keys(e),i=n.length;for(;i-- >0;)if(t===(r=n[i]).toLowerCase())return r;return null}let j=/*eslint no-undef:0*/"undefined"!=typeof globalThis?globalThis:"undefined"!=typeof self?self:"undefined"!=typeof window?window:a,N=e=>!m(e)&&e!==j,P=(r="undefined"!=typeof Uint8Array&&c(Uint8Array),e=>r&&e instanceof r),_=f("HTMLFormElement"),U=(({hasOwnProperty:e})=>(t,r)=>e.call(t,r))(Object.prototype),F=f("RegExp"),L=(e,t)=>{let r=Object.getOwnPropertyDescriptors(e),n={};C(r,(r,i)=>{let o;!1!==(o=t(r,i,e))&&(n[i]=o||r)}),Object.defineProperties(e,n)},D="abcdefghijklmnopqrstuvwxyz",B="0123456789",k={DIGIT:B,ALPHA:D,ALPHA_DIGIT:D+D.toUpperCase()+B},z=f("AsyncFunction");var I={isArray:h,isArrayBuffer:g,isBuffer:/**
 * Determine if a value is a Buffer
 *
 * @param {*} val The value to test
 *
 * @returns {boolean} True if value is a Buffer, otherwise false
 */function(e){return null!==e&&!m(e)&&null!==e.constructor&&!m(e.constructor)&&b(e.constructor.isBuffer)&&e.constructor.isBuffer(e)},isFormData:e=>{let t;return e&&("function"==typeof FormData&&e instanceof FormData||b(e.append)&&("formdata"===(t=d(e))||// detect form-data instance
"object"===t&&b(e.toString)&&"[object FormData]"===e.toString()))},isArrayBufferView:/**
 * Determine if a value is a view on an ArrayBuffer
 *
 * @param {*} val The value to test
 *
 * @returns {boolean} True if value is a view on an ArrayBuffer, otherwise false
 */function(e){return"undefined"!=typeof ArrayBuffer&&ArrayBuffer.isView?ArrayBuffer.isView(e):e&&e.buffer&&g(e.buffer)},isString:y,isNumber:E,isBoolean:e=>!0===e||!1===e,isObject:w,isPlainObject:O,isUndefined:m,isDate:S,isFile:v,isBlob:R,isRegExp:F,isFunction:b,isStream:e=>w(e)&&b(e.pipe),isURLSearchParams:T,isTypedArray:P,isFileList:A,forEach:C,merge:/**
 * Accepts varargs expecting each argument to be an object, then
 * immutably merges the properties of each object and returns result.
 *
 * When multiple objects contain the same key the later object in
 * the arguments list will take precedence.
 *
 * Example:
 *
 * ```js
 * var result = merge({foo: 123}, {foo: 456});
 * console.log(result.foo); // outputs 456
 * ```
 *
 * @param {Object} obj1 Object to merge
 *
 * @returns {Object} Result of all merge properties
 */function e(){let{caseless:t}=N(this)&&this||{},r={},n=(n,i)=>{let o=t&&x(r,i)||i;O(r[o])&&O(n)?r[o]=e(r[o],n):O(n)?r[o]=e({},n):h(n)?r[o]=n.slice():r[o]=n};for(let e=0,t=arguments.length;e<t;e++)arguments[e]&&C(arguments[e],n);return r},extend:(e,t,r,{allOwnKeys:n}={})=>(C(t,(t,n)=>{r&&b(t)?e[n]=l(t,r):e[n]=t},{allOwnKeys:n}),e),trim:e=>e.trim?e.trim():e.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,""),stripBOM:e=>(65279===e.charCodeAt(0)&&(e=e.slice(1)),e),inherits:(e,t,r,n)=>{e.prototype=Object.create(t.prototype,n),e.prototype.constructor=e,Object.defineProperty(e,"super",{value:t.prototype}),r&&Object.assign(e.prototype,r)},toFlatObject:(e,t,r,n)=>{let i,o,s;let a={};// eslint-disable-next-line no-eq-null,eqeqeq
if(t=t||{},null==e)return t;do{for(o=(i=Object.getOwnPropertyNames(e)).length;o-- >0;)s=i[o],(!n||n(s,e,t))&&!a[s]&&(t[s]=e[s],a[s]=!0);e=!1!==r&&c(e)}while(e&&(!r||r(e,t))&&e!==Object.prototype)return t},kindOf:d,kindOfTest:f,endsWith:(e,t,r)=>{e=String(e),(void 0===r||r>e.length)&&(r=e.length),r-=t.length;let n=e.indexOf(t,r);return -1!==n&&n===r},toArray:e=>{if(!e)return null;if(h(e))return e;let t=e.length;if(!E(t))return null;let r=Array(t);for(;t-- >0;)r[t]=e[t];return r},forEachEntry:(e,t)=>{let r;let n=e&&e[Symbol.iterator],i=n.call(e);for(;(r=i.next())&&!r.done;){let n=r.value;t.call(e,n[0],n[1])}},matchAll:(e,t)=>{let r;let n=[];for(;null!==(r=e.exec(t));)n.push(r);return n},isHTMLForm:_,hasOwnProperty:U,hasOwnProp:U,reduceDescriptors:L,freezeMethods:e=>{L(e,(t,r)=>{// skip restricted props in strict mode
if(b(e)&&-1!==["arguments","caller","callee"].indexOf(r))return!1;let n=e[r];if(b(n)){if(t.enumerable=!1,"writable"in t){t.writable=!1;return}t.set||(t.set=()=>{throw Error("Can not rewrite read-only method '"+r+"'")})}})},toObjectSet:(e,t)=>{let r={};return(e=>{e.forEach(e=>{r[e]=!0})})(h(e)?e:String(e).split(t)),r},toCamelCase:e=>e.toLowerCase().replace(/[-_\s]([a-z\d])(\w*)/g,function(e,t,r){return t.toUpperCase()+r}),noop:()=>{},toFiniteNumber:(e,t)=>Number.isFinite(e=+e)?e:t,findKey:x,global:j,isContextDefined:N,ALPHABET:k,generateString:(e=16,t=k.ALPHA_DIGIT)=>{let r="",{length:n}=t;for(;e--;)r+=t[Math.random()*n|0];return r},isSpecCompliantForm:/**
 * If the thing is a FormData object, return true, otherwise return false.
 *
 * @param {unknown} thing - The thing to check.
 *
 * @returns {boolean}
 */function(e){return!!(e&&b(e.append)&&"FormData"===e[Symbol.toStringTag]&&e[Symbol.iterator])},toJSONObject:e=>{let t=Array(10),r=(e,n)=>{if(w(e)){if(t.indexOf(e)>=0)return;if(!("toJSON"in e)){t[n]=e;let i=h(e)?[]:{};return C(e,(e,t)=>{let o=r(e,n+1);m(o)||(i[t]=o)}),t[n]=void 0,i}}return e};return r(e,0)},isAsyncFn:z,isThenable:e=>e&&(w(e)||b(e))&&b(e.then)&&b(e.catch)};/**
 * Create an Error with the specified message, config, error code, request and response.
 *
 * @param {string} message The error message.
 * @param {string} [code] The error code (for example, 'ECONNABORTED').
 * @param {Object} [config] The config.
 * @param {Object} [request] The request.
 * @param {Object} [response] The response.
 *
 * @returns {Error} The created error.
 */function q(e,t,r,n,i){Error.call(this),Error.captureStackTrace?Error.captureStackTrace(this,this.constructor):this.stack=Error().stack,this.message=e,this.name="AxiosError",t&&(this.code=t),r&&(this.config=r),n&&(this.request=n),i&&(this.response=i)}I.inherits(q,Error,{toJSON:function(){return{// Standard
message:this.message,name:this.name,// Microsoft
description:this.description,number:this.number,// Mozilla
fileName:this.fileName,lineNumber:this.lineNumber,columnNumber:this.columnNumber,stack:this.stack,// Axios
config:I.toJSONObject(this.config),code:this.code,status:this.response&&this.response.status?this.response.status:null}}});let M=q.prototype,H={};["ERR_BAD_OPTION_VALUE","ERR_BAD_OPTION","ECONNABORTED","ETIMEDOUT","ERR_NETWORK","ERR_FR_TOO_MANY_REDIRECTS","ERR_DEPRECATED","ERR_BAD_RESPONSE","ERR_BAD_REQUEST","ERR_CANCELED","ERR_NOT_SUPPORT","ERR_INVALID_URL"].forEach(e=>{H[e]={value:e}}),Object.defineProperties(q,H),Object.defineProperty(M,"isAxiosError",{value:!0}),// eslint-disable-next-line func-names
q.from=(e,t,r,n,i,o)=>{let s=Object.create(M);return I.toFlatObject(e,s,function(e){return e!==Error.prototype},e=>"isAxiosError"!==e),q.call(s,e.message,t,r,n,i),s.cause=e,s.name=e.name,o&&Object.assign(s,o),s};var J={}.Buffer;/**
 * Determines if the given thing is a array or js object.
 *
 * @param {string} thing - The object or array to be visited.
 *
 * @returns {boolean}
 */function $(e){return I.isPlainObject(e)||I.isArray(e)}/**
 * It removes the brackets from the end of a string
 *
 * @param {string} key - The key of the parameter.
 *
 * @returns {string} the key without the brackets.
 */function W(e){return I.endsWith(e,"[]")?e.slice(0,-2):e}/**
 * It takes a path, a key, and a boolean, and returns a string
 *
 * @param {string} path - The path to the current key.
 * @param {string} key - The key of the current object being iterated over.
 * @param {string} dots - If true, the key will be rendered with dots instead of brackets.
 *
 * @returns {string} The path to the current key.
 */function V(e,t,r){return e?e.concat(t).map(function(e,t){return(// eslint-disable-next-line no-param-reassign
e=W(e),!r&&t?"["+e+"]":e)}).join(r?".":""):t}let K=I.toFlatObject(I,{},null,function(e){return/^is[A-Z]/.test(e)});var G=/**
 * Convert a data object to FormData
 *
 * @param {Object} obj
 * @param {?Object} [formData]
 * @param {?Object} [options]
 * @param {Function} [options.visitor]
 * @param {Boolean} [options.metaTokens = true]
 * @param {Boolean} [options.dots = false]
 * @param {?Boolean} [options.indexes = false]
 *
 * @returns {Object}
 **//**
 * It converts an object into a FormData object
 *
 * @param {Object<any, any>} obj - The object to convert to form data.
 * @param {string} formData - The FormData object to append to.
 * @param {Object<string, any>} options
 *
 * @returns
 */function(e,t,r){if(!I.isObject(e))throw TypeError("target must be an object");// eslint-disable-next-line no-param-reassign
t=t||new FormData,// eslint-disable-next-line no-param-reassign
r=I.toFlatObject(r,{metaTokens:!0,dots:!1,indexes:!1},!1,function(e,t){// eslint-disable-next-line no-eq-null,eqeqeq
return!I.isUndefined(t[e])});let n=r.metaTokens,i=r.visitor||c,o=r.dots,s=r.indexes,a=r.Blob||"undefined"!=typeof Blob&&Blob,l=a&&I.isSpecCompliantForm(t);if(!I.isFunction(i))throw TypeError("visitor must be a function");function u(e){if(null===e)return"";if(I.isDate(e))return e.toISOString();if(!l&&I.isBlob(e))throw new q("Blob is not supported. Use a Buffer instead.");return I.isArrayBuffer(e)||I.isTypedArray(e)?l&&"function"==typeof Blob?new Blob([e]):J.from(e):e}/**
   * Default visitor.
   *
   * @param {*} value
   * @param {String|Number} key
   * @param {Array<String|Number>} path
   * @this {FormData}
   *
   * @returns {boolean} return true to visit the each prop of the value recursively
   */function c(e,r,i){let a=e;if(e&&!i&&"object"==typeof e){if(I.endsWith(r,"{}"))// eslint-disable-next-line no-param-reassign
r=n?r:r.slice(0,-2),// eslint-disable-next-line no-param-reassign
e=JSON.stringify(e);else{var l;if(I.isArray(e)&&(l=e,I.isArray(l)&&!l.some($))||(I.isFileList(e)||I.endsWith(r,"[]"))&&(a=I.toArray(e)))return(// eslint-disable-next-line no-param-reassign
r=W(r),a.forEach(function(e,n){I.isUndefined(e)||null===e||t.append(!0===s?V([r],n,o):null===s?r:r+"[]",u(e))}),!1)}}return!!$(e)||(t.append(V(i,r,o),u(e)),!1)}let d=[],f=Object.assign(K,{defaultVisitor:c,convertValue:u,isVisitable:$});if(!I.isObject(e))throw TypeError("data must be an object");return!function e(r,n){if(!I.isUndefined(r)){if(-1!==d.indexOf(r))throw Error("Circular reference detected in "+n.join("."));d.push(r),I.forEach(r,function(r,o){let s=!(I.isUndefined(r)||null===r)&&i.call(t,r,I.isString(o)?o.trim():o,n,f);!0===s&&e(r,n?n.concat(o):[o])}),d.pop()}}(e),t};/**
 * It encodes a string by replacing all characters that are not in the unreserved set with
 * their percent-encoded equivalents
 *
 * @param {string} str - The string to encode.
 *
 * @returns {string} The encoded string.
 */function X(e){let t={"!":"%21","'":"%27","(":"%28",")":"%29","~":"%7E","%20":"+","%00":"\x00"};return encodeURIComponent(e).replace(/[!'()~]|%20|%00/g,function(e){return t[e]})}/**
 * It takes a params object and converts it to a FormData object
 *
 * @param {Object<string, any>} params - The parameters to be converted to a FormData object.
 * @param {Object<string, any>} options - The options object passed to the Axios constructor.
 *
 * @returns {void}
 */function Q(e,t){this._pairs=[],e&&G(e,this,t)}let Z=Q.prototype;/**
 * It replaces all instances of the characters `:`, `$`, `,`, `+`, `[`, and `]` with their
 * URI encoded counterparts
 *
 * @param {string} val The value to be encoded.
 *
 * @returns {string} The encoded value.
 */function Y(e){return encodeURIComponent(e).replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%20/g,"+").replace(/%5B/gi,"[").replace(/%5D/gi,"]")}function ee(e,t,r){let n;/*eslint no-param-reassign:0*/if(!t)return e;let i=r&&r.encode||Y,o=r&&r.serialize;if(n=o?o(t,r):I.isURLSearchParams(t)?t.toString():new Q(t,r).toString(i)){let t=e.indexOf("#");-1!==t&&(e=e.slice(0,t)),e+=(-1===e.indexOf("?")?"?":"&")+n}return e}Z.append=function(e,t){this._pairs.push([e,t])},Z.toString=function(e){let t=e?function(t){return e.call(this,t,X)}:X;return this._pairs.map(function(e){return t(e[0])+"="+t(e[1])},"").join("&")};var et=class{constructor(){this.handlers=[]}/**
   * Add a new interceptor to the stack
   *
   * @param {Function} fulfilled The function to handle `then` for a `Promise`
   * @param {Function} rejected The function to handle `reject` for a `Promise`
   *
   * @return {Number} An ID used to remove interceptor later
   */use(e,t,r){return this.handlers.push({fulfilled:e,rejected:t,synchronous:!!r&&r.synchronous,runWhen:r?r.runWhen:null}),this.handlers.length-1}/**
   * Remove an interceptor from the stack
   *
   * @param {Number} id The ID that was returned by `use`
   *
   * @returns {Boolean} `true` if the interceptor was removed, `false` otherwise
   */eject(e){this.handlers[e]&&(this.handlers[e]=null)}/**
   * Clear all interceptors from the stack
   *
   * @returns {void}
   */clear(){this.handlers&&(this.handlers=[])}/**
   * Iterate over all the registered interceptors
   *
   * This method is particularly useful for skipping over any
   * interceptors that may have become `null` calling `eject`.
   *
   * @param {Function} fn The function to call for each interceptor
   *
   * @returns {void}
   */forEach(e){I.forEach(this.handlers,function(t){null!==t&&e(t)})}},er={silentJSONParsing:!0,forcedJSONParsing:!0,clarifyTimeoutError:!1},en="undefined"!=typeof URLSearchParams?URLSearchParams:Q,ei="undefined"!=typeof FormData?FormData:null,eo="undefined"!=typeof Blob?Blob:null;/**
 * Determine if we're running in a standard browser environment
 *
 * This allows axios to run in a web worker, and react-native.
 * Both environments support XMLHttpRequest, but not fully standard globals.
 *
 * web workers:
 *  typeof window -> undefined
 *  typeof document -> undefined
 *
 * react-native:
 *  navigator.product -> 'ReactNative'
 * nativescript
 *  navigator.product -> 'NativeScript' or 'NS'
 *
 * @returns {boolean}
 */let es=("undefined"==typeof navigator||"ReactNative"!==(e=navigator.product)&&"NativeScript"!==e&&"NS"!==e)&&"undefined"!=typeof window&&"undefined"!=typeof document,ea="undefined"!=typeof WorkerGlobalScope&&// eslint-disable-next-line no-undef
self instanceof WorkerGlobalScope&&"function"==typeof self.importScripts;var el={classes:{URLSearchParams:en,FormData:ei,Blob:eo},isStandardBrowserEnv:es,isStandardBrowserWebWorkerEnv:ea,protocols:["http","https","file","blob","url","data"]},eu=/**
 * It takes a FormData object and returns a JavaScript object
 *
 * @param {string} formData The FormData object to convert to JSON.
 *
 * @returns {Object<string, any> | null} The converted object.
 */function(e){if(I.isFormData(e)&&I.isFunction(e.entries)){let t={};return I.forEachEntry(e,(e,r)=>{!function e(t,r,n,i){let o=t[i++],s=Number.isFinite(+o),a=i>=t.length;if(o=!o&&I.isArray(n)?n.length:o,a)return I.hasOwnProp(n,o)?n[o]=[n[o],r]:n[o]=r,!s;n[o]&&I.isObject(n[o])||(n[o]=[]);let l=e(t,r,n[o],i);return l&&I.isArray(n[o])&&(n[o]=/**
 * Convert an array to an object.
 *
 * @param {Array<any>} arr - The array to convert to an object.
 *
 * @returns An object with the same keys and values as the array.
 */function(e){let t,r;let n={},i=Object.keys(e),o=i.length;for(t=0;t<o;t++)n[r=i[t]]=e[r];return n}(n[o])),!s}(I.matchAll(/\w+|\[(\w*)]/g,e).map(e=>"[]"===e[0]?"":e[1]||e[0]),r,t,0)}),t}return null};let ec={transitional:er,adapter:["xhr","http"],transformRequest:[function(e,t){let r;let n=t.getContentType()||"",i=n.indexOf("application/json")>-1,o=I.isObject(e);o&&I.isHTMLForm(e)&&(e=new FormData(e));let s=I.isFormData(e);if(s)return i&&i?JSON.stringify(eu(e)):e;if(I.isArrayBuffer(e)||I.isBuffer(e)||I.isStream(e)||I.isFile(e)||I.isBlob(e))return e;if(I.isArrayBufferView(e))return e.buffer;if(I.isURLSearchParams(e))return t.setContentType("application/x-www-form-urlencoded;charset=utf-8",!1),e.toString();if(o){if(n.indexOf("application/x-www-form-urlencoded")>-1){var a,l;return(a=e,l=this.formSerializer,G(a,new el.classes.URLSearchParams,Object.assign({visitor:function(e,t,r,n){return el.isNode&&I.isBuffer(e)?(this.append(t,e.toString("base64")),!1):n.defaultVisitor.apply(this,arguments)}},l))).toString()}if((r=I.isFileList(e))||n.indexOf("multipart/form-data")>-1){let t=this.env&&this.env.FormData;return G(r?{"files[]":e}:e,t&&new t,this.formSerializer)}}return o||i?(t.setContentType("application/json",!1),/**
 * It takes a string, tries to parse it, and if it fails, it returns the stringified version
 * of the input
 *
 * @param {any} rawValue - The value to be stringified.
 * @param {Function} parser - A function that parses a string into a JavaScript object.
 * @param {Function} encoder - A function that takes a value and returns a string.
 *
 * @returns {string} A stringified version of the rawValue.
 */function(e,t,r){if(I.isString(e))try{return(0,JSON.parse)(e),I.trim(e)}catch(e){if("SyntaxError"!==e.name)throw e}return(0,JSON.stringify)(e)}(e)):e}],transformResponse:[function(e){let t=this.transitional||ec.transitional,r=t&&t.forcedJSONParsing,n="json"===this.responseType;if(e&&I.isString(e)&&(r&&!this.responseType||n)){let r=t&&t.silentJSONParsing;try{return JSON.parse(e)}catch(e){if(!r&&n){if("SyntaxError"===e.name)throw q.from(e,q.ERR_BAD_RESPONSE,this,null,this.response);throw e}}}return e}],/**
   * A timeout in milliseconds to abort a request. If set to 0 (default) a
   * timeout is not created.
   */timeout:0,xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN",maxContentLength:-1,maxBodyLength:-1,env:{FormData:el.classes.FormData,Blob:el.classes.Blob},validateStatus:function(e){return e>=200&&e<300},headers:{common:{Accept:"application/json, text/plain, */*","Content-Type":void 0}}};I.forEach(["delete","get","head","post","put","patch"],e=>{ec.headers[e]={}});// RawAxiosHeaders whose duplicates are ignored by node
// c.f. https://nodejs.org/api/http.html#http_message_headers
let ed=I.toObjectSet(["age","authorization","content-length","content-type","etag","expires","from","host","if-modified-since","if-unmodified-since","last-modified","location","max-forwards","proxy-authorization","referer","retry-after","user-agent"]);var /**
 * Parse headers into an object
 *
 * ```
 * Date: Wed, 27 Aug 2014 08:58:49 GMT
 * Content-Type: application/json
 * Connection: keep-alive
 * Transfer-Encoding: chunked
 * ```
 *
 * @param {String} rawHeaders Headers needing to be parsed
 *
 * @returns {Object} Headers parsed into an object
 */ef=e=>{let t,r,n;let i={};return e&&e.split("\n").forEach(function(e){n=e.indexOf(":"),t=e.substring(0,n).trim().toLowerCase(),r=e.substring(n+1).trim(),!t||i[t]&&ed[t]||("set-cookie"===t?i[t]?i[t].push(r):i[t]=[r]:i[t]=i[t]?i[t]+", "+r:r)}),i};let ep=Symbol("internals");function eh(e){return e&&String(e).trim().toLowerCase()}function em(e){return!1===e||null==e?e:I.isArray(e)?e.map(em):String(e)}let eg=e=>/^[-_a-zA-Z0-9^`|~,!#$%&'*+.]+$/.test(e.trim());function ey(e,t,r,n,i){if(I.isFunction(n))return n.call(this,t,r);if(i&&(t=r),I.isString(t)){if(I.isString(n))return -1!==t.indexOf(n);if(I.isRegExp(n))return n.test(t)}}class eb{constructor(e){e&&this.set(e)}set(e,t,r){let n=this;function i(e,t,r){let i=eh(t);if(!i)throw Error("header name must be a non-empty string");let o=I.findKey(n,i);o&&void 0!==n[o]&&!0!==r&&(void 0!==r||!1===n[o])||(n[o||t]=em(e))}let o=(e,t)=>I.forEach(e,(e,r)=>i(e,r,t));return I.isPlainObject(e)||e instanceof this.constructor?o(e,t):I.isString(e)&&(e=e.trim())&&!eg(e)?o(ef(e),t):null!=e&&i(t,e,r),this}get(e,t){if(e=eh(e)){let r=I.findKey(this,e);if(r){let e=this[r];if(!t)return e;if(!0===t)return function(e){let t;let r=Object.create(null),n=/([^\s,;=]+)\s*(?:=\s*([^,;]+))?/g;for(;t=n.exec(e);)r[t[1]]=t[2];return r}(e);if(I.isFunction(t))return t.call(this,e,r);if(I.isRegExp(t))return t.exec(e);throw TypeError("parser must be boolean|regexp|function")}}}has(e,t){if(e=eh(e)){let r=I.findKey(this,e);return!!(r&&void 0!==this[r]&&(!t||ey(this,this[r],r,t)))}return!1}delete(e,t){let r=this,n=!1;function i(e){if(e=eh(e)){let i=I.findKey(r,e);i&&(!t||ey(r,r[i],i,t))&&(delete r[i],n=!0)}}return I.isArray(e)?e.forEach(i):i(e),n}clear(e){let t=Object.keys(this),r=t.length,n=!1;for(;r--;){let i=t[r];(!e||ey(this,this[i],i,e,!0))&&(delete this[i],n=!0)}return n}normalize(e){let t=this,r={};return I.forEach(this,(n,i)=>{let o=I.findKey(r,i);if(o){t[o]=em(n),delete t[i];return}let s=e?i.trim().toLowerCase().replace(/([a-z\d])(\w*)/g,(e,t,r)=>t.toUpperCase()+r):String(i).trim();s!==i&&delete t[i],t[s]=em(n),r[s]=!0}),this}concat(...e){return this.constructor.concat(this,...e)}toJSON(e){let t=Object.create(null);return I.forEach(this,(r,n)=>{null!=r&&!1!==r&&(t[n]=e&&I.isArray(r)?r.join(", "):r)}),t}[Symbol.iterator](){return Object.entries(this.toJSON())[Symbol.iterator]()}toString(){return Object.entries(this.toJSON()).map(([e,t])=>e+": "+t).join("\n")}get[Symbol.toStringTag](){return"AxiosHeaders"}static from(e){return e instanceof this?e:new this(e)}static concat(e,...t){let r=new this(e);return t.forEach(e=>r.set(e)),r}static accessor(e){let t=this[ep]=this[ep]={accessors:{}},r=t.accessors,n=this.prototype;function i(e){let t=eh(e);r[t]||(!function(e,t){let r=I.toCamelCase(" "+t);["get","set","has"].forEach(n=>{Object.defineProperty(e,n+r,{value:function(e,r,i){return this[n].call(this,t,e,r,i)},configurable:!0})})}(n,e),r[t]=!0)}return I.isArray(e)?e.forEach(i):i(e),this}}function eE(e,t){let r=this||ec,n=t||r,i=eb.from(n.headers),o=n.data;return I.forEach(e,function(e){o=e.call(r,o,i.normalize(),t?t.status:void 0)}),i.normalize(),o}function ew(e){return!!(e&&e.__CANCEL__)}/**
 * A `CanceledError` is an object that is thrown when an operation is canceled.
 *
 * @param {string=} message The message.
 * @param {Object=} config The config.
 * @param {Object=} request The request.
 *
 * @returns {CanceledError} The created error.
 */function eO(e,t,r){q.call(this,null==e?"canceled":e,q.ERR_CANCELED,t,r),this.name="CanceledError"}eb.accessor(["Content-Type","Content-Length","Accept","Accept-Encoding","User-Agent","Authorization"]),I.reduceDescriptors(eb.prototype,({value:e},t)=>{let r=t[0].toUpperCase()+t.slice(1);// map `set` => `Set`
return{get:()=>e,set(e){this[r]=e}}}),I.freezeMethods(eb),I.inherits(eO,q,{__CANCEL__:!0});var eS=el.isStandardBrowserEnv?{write:function(e,t,r,n,i,o){let s=[];s.push(e+"="+encodeURIComponent(t)),I.isNumber(r)&&s.push("expires="+new Date(r).toGMTString()),I.isString(n)&&s.push("path="+n),I.isString(i)&&s.push("domain="+i),!0===o&&s.push("secure"),document.cookie=s.join("; ")},read:function(e){let t=document.cookie.match(RegExp("(^|;\\s*)("+e+")=([^;]*)"));return t?decodeURIComponent(t[3]):null},remove:function(e){this.write(e,"",Date.now()-864e5)}}:{write:function(){},read:function(){return null},remove:function(){}};function ev(e,t){return e&&!/^([a-z][a-z\d+\-.]*:)?\/\//i.test(t)?t?e.replace(/\/+$/,"")+"/"+t.replace(/^\/+/,""):e:t}var eR=el.isStandardBrowserEnv?// whether the request URL is of the same origin as current location.
function(){let e;let t=/(msie|trident)/i.test(navigator.userAgent),r=document.createElement("a");/**
    * Parse a URL to discover it's components
    *
    * @param {String} url The URL to be parsed
    * @returns {Object}
    */function n(e){let n=e;// urlParsingNode provides the UrlUtils interface - http://url.spec.whatwg.org/#urlutils
return t&&(// IE needs attribute set twice to normalize properties
r.setAttribute("href",n),n=r.href),r.setAttribute("href",n),{href:r.href,protocol:r.protocol?r.protocol.replace(/:$/,""):"",host:r.host,search:r.search?r.search.replace(/^\?/,""):"",hash:r.hash?r.hash.replace(/^#/,""):"",hostname:r.hostname,port:r.port,pathname:"/"===r.pathname.charAt(0)?r.pathname:"/"+r.pathname}}/**
    * Determine if a URL shares the same origin as the current location
    *
    * @param {String} requestURL The URL to test
    * @returns {boolean} True if URL shares the same origin, otherwise false
    */return e=n(window.location.href),function(t){let r=I.isString(t)?n(t):t;return r.protocol===e.protocol&&r.host===e.host}}():function(){return!0},eA=/**
 * Calculate data maxRate
 * @param {Number} [samplesCount= 10]
 * @param {Number} [min= 1000]
 * @returns {Function}
 */function(e,t){let r;e=e||10;let n=Array(e),i=Array(e),o=0,s=0;return t=void 0!==t?t:1e3,function(a){let l=Date.now(),u=i[s];r||(r=l),n[o]=a,i[o]=l;let c=s,d=0;for(;c!==o;)d+=n[c++],c%=e;if((o=(o+1)%e)===s&&(s=(s+1)%e),l-r<t)return;let f=u&&l-u;return f?Math.round(1e3*d/f):void 0}};function eT(e,t){let r=0,n=eA(50,250);return i=>{let o=i.loaded,s=i.lengthComputable?i.total:void 0,a=o-r,l=n(a),u=o<=s;r=o;let c={loaded:o,total:s,progress:s?o/s:void 0,bytes:a,rate:l||void 0,estimated:l&&s&&u?(s-o)/l:void 0,event:i};c[t?"download":"upload"]=!0,e(c)}}let eC="undefined"!=typeof XMLHttpRequest;var ex=eC&&function(e){return new Promise(function(t,r){let n,i,o=e.data,s=eb.from(e.headers).normalize(),a=e.responseType;function l(){e.cancelToken&&e.cancelToken.unsubscribe(n),e.signal&&e.signal.removeEventListener("abort",n)}I.isFormData(o)&&(el.isStandardBrowserEnv||el.isStandardBrowserWebWorkerEnv?s.setContentType(!1):s.getContentType(/^\s*multipart\/form-data/)?I.isString(i=s.getContentType())&&s.setContentType(i.replace(/^\s*(multipart\/form-data);+/,"$1")):s.setContentType("multipart/form-data"));let u=new XMLHttpRequest;// HTTP basic authentication
if(e.auth){let t=e.auth.username||"",r=e.auth.password?unescape(encodeURIComponent(e.auth.password)):"";s.set("Authorization","Basic "+btoa(t+":"+r))}let c=ev(e.baseURL,e.url);function d(){if(!u)return;// Prepare the response
let n=eb.from("getAllResponseHeaders"in u&&u.getAllResponseHeaders()),i=a&&"text"!==a&&"json"!==a?u.response:u.responseText,o={data:i,status:u.status,statusText:u.statusText,headers:n,config:e,request:u};!function(e,t,r){let n=r.config.validateStatus;!r.status||!n||n(r.status)?e(r):t(new q("Request failed with status code "+r.status,[q.ERR_BAD_REQUEST,q.ERR_BAD_RESPONSE][Math.floor(r.status/100)-4],r.config,r.request,r))}(function(e){t(e),l()},function(e){r(e),l()},o),// Clean up request
u=null}// Add xsrf header
// This is only done if running in a standard browser environment.
// Specifically not if we're in a web worker, or react-native.
if(u.open(e.method.toUpperCase(),ee(c,e.params,e.paramsSerializer),!0),// Set the request timeout in MS
u.timeout=e.timeout,"onloadend"in u?u.onloadend=d:u.onreadystatechange=function(){u&&4===u.readyState&&(0!==u.status||u.responseURL&&0===u.responseURL.indexOf("file:"))&&// readystate handler is calling before onerror or ontimeout handlers,
// so we should call onloadend on the next 'tick'
setTimeout(d)},// Handle browser request cancellation (as opposed to a manual cancellation)
u.onabort=function(){u&&(r(new q("Request aborted",q.ECONNABORTED,e,u)),// Clean up request
u=null)},// Handle low level network errors
u.onerror=function(){// Real errors are hidden from us by the browser
// onerror should only fire if it's a network error
r(new q("Network Error",q.ERR_NETWORK,e,u)),// Clean up request
u=null},// Handle timeout
u.ontimeout=function(){let t=e.timeout?"timeout of "+e.timeout+"ms exceeded":"timeout exceeded",n=e.transitional||er;e.timeoutErrorMessage&&(t=e.timeoutErrorMessage),r(new q(t,n.clarifyTimeoutError?q.ETIMEDOUT:q.ECONNABORTED,e,u)),// Clean up request
u=null},el.isStandardBrowserEnv){// Add xsrf header
let t=(e.withCredentials||eR(c))&&e.xsrfCookieName&&eS.read(e.xsrfCookieName);t&&s.set(e.xsrfHeaderName,t)}// Remove Content-Type if data is undefined
void 0===o&&s.setContentType(null),"setRequestHeader"in u&&I.forEach(s.toJSON(),function(e,t){u.setRequestHeader(t,e)}),I.isUndefined(e.withCredentials)||(u.withCredentials=!!e.withCredentials),a&&"json"!==a&&(u.responseType=e.responseType),"function"==typeof e.onDownloadProgress&&u.addEventListener("progress",eT(e.onDownloadProgress,!0)),"function"==typeof e.onUploadProgress&&u.upload&&u.upload.addEventListener("progress",eT(e.onUploadProgress)),(e.cancelToken||e.signal)&&(// Handle cancellation
// eslint-disable-next-line func-names
n=t=>{u&&(r(!t||t.type?new eO(null,e,u):t),u.abort(),u=null)},e.cancelToken&&e.cancelToken.subscribe(n),e.signal&&(e.signal.aborted?n():e.signal.addEventListener("abort",n)));let f=function(e){let t=/^([-+\w]{1,25})(:?\/\/|:)/.exec(e);return t&&t[1]||""}(c);if(f&&-1===el.protocols.indexOf(f)){r(new q("Unsupported protocol "+f+":",q.ERR_BAD_REQUEST,e));return}// Send the request
u.send(o||null)})};let ej={http:null,xhr:ex};I.forEach(ej,(e,t)=>{if(e){try{Object.defineProperty(e,"name",{value:t})}catch(e){// eslint-disable-next-line no-empty
}Object.defineProperty(e,"adapterName",{value:t})}});let eN=e=>`- ${e}`,eP=e=>I.isFunction(e)||null===e||!1===e;var e_={getAdapter:e=>{let t,r;e=I.isArray(e)?e:[e];let{length:n}=e,i={};for(let o=0;o<n;o++){let n;if(r=t=e[o],!eP(t)&&void 0===(r=ej[(n=String(t)).toLowerCase()]))throw new q(`Unknown adapter '${n}'`);if(r)break;i[n||"#"+o]=r}if(!r){let e=Object.entries(i).map(([e,t])=>`adapter ${e} `+(!1===t?"is not supported by the environment":"is not available in the build")),t=n?e.length>1?"since :\n"+e.map(eN).join("\n"):" "+eN(e[0]):"as no adapter specified";throw new q("There is no suitable adapter to dispatch the request "+t,"ERR_NOT_SUPPORT")}return r},adapters:ej};/**
 * Throws a `CanceledError` if cancellation has been requested.
 *
 * @param {Object} config The config that is to be used for the request
 *
 * @returns {void}
 */function eU(e){if(e.cancelToken&&e.cancelToken.throwIfRequested(),e.signal&&e.signal.aborted)throw new eO(null,e)}function eF(e){eU(e),e.headers=eb.from(e.headers),// Transform request data
e.data=eE.call(e,e.transformRequest),-1!==["post","put","patch"].indexOf(e.method)&&e.headers.setContentType("application/x-www-form-urlencoded",!1);let t=e_.getAdapter(e.adapter||ec.adapter);return t(e).then(function(t){return eU(e),// Transform response data
t.data=eE.call(e,e.transformResponse,t),t.headers=eb.from(t.headers),t},function(t){return!ew(t)&&(eU(e),t&&t.response&&(t.response.data=eE.call(e,e.transformResponse,t.response),t.response.headers=eb.from(t.response.headers))),Promise.reject(t)})}let eL=e=>e instanceof eb?e.toJSON():e;function eD(e,t){// eslint-disable-next-line no-param-reassign
t=t||{};let r={};function n(e,t,r){return I.isPlainObject(e)&&I.isPlainObject(t)?I.merge.call({caseless:r},e,t):I.isPlainObject(t)?I.merge({},t):I.isArray(t)?t.slice():t}// eslint-disable-next-line consistent-return
function i(e,t,r){return I.isUndefined(t)?I.isUndefined(e)?void 0:n(void 0,e,r):n(e,t,r)}// eslint-disable-next-line consistent-return
function o(e,t){if(!I.isUndefined(t))return n(void 0,t)}// eslint-disable-next-line consistent-return
function s(e,t){return I.isUndefined(t)?I.isUndefined(e)?void 0:n(void 0,e):n(void 0,t)}// eslint-disable-next-line consistent-return
function a(r,i,o){return o in t?n(r,i):o in e?n(void 0,r):void 0}let l={url:o,method:o,data:o,baseURL:s,transformRequest:s,transformResponse:s,paramsSerializer:s,timeout:s,timeoutMessage:s,withCredentials:s,adapter:s,responseType:s,xsrfCookieName:s,xsrfHeaderName:s,onUploadProgress:s,onDownloadProgress:s,decompress:s,maxContentLength:s,maxBodyLength:s,beforeRedirect:s,transport:s,httpAgent:s,httpsAgent:s,cancelToken:s,socketPath:s,responseEncoding:s,validateStatus:a,headers:(e,t)=>i(eL(e),eL(t),!0)};return I.forEach(Object.keys(Object.assign({},e,t)),function(n){let o=l[n]||i,s=o(e[n],t[n],n);I.isUndefined(s)&&o!==a||(r[n]=s)}),r}let eB="1.5.1",ek={};// eslint-disable-next-line func-names
["object","boolean","number","function","string","symbol"].forEach((e,t)=>{ek[e]=function(r){return typeof r===e||"a"+(t<1?"n ":" ")+e}});let ez={};/**
 * Transitional option validator
 *
 * @param {function|boolean?} validator - set to false if the transitional option has been removed
 * @param {string?} version - deprecated version / removed since version
 * @param {string?} message - some message with additional info
 *
 * @returns {function}
 */ek.transitional=function(e,t,r){function n(e,t){return"[Axios v"+eB+"] Transitional option '"+e+"'"+t+(r?". "+r:"")}// eslint-disable-next-line func-names
return(r,i,o)=>{if(!1===e)throw new q(n(i," has been removed"+(t?" in "+t:"")),q.ERR_DEPRECATED);return t&&!ez[i]&&(ez[i]=!0,// eslint-disable-next-line no-console
console.warn(n(i," has been deprecated since v"+t+" and will be removed in the near future"))),!e||e(r,i,o)}};var eI={assertOptions:/**
 * Assert object's properties type
 *
 * @param {object} options
 * @param {object} schema
 * @param {boolean?} allowUnknown
 *
 * @returns {object}
 */function(e,t,r){if("object"!=typeof e)throw new q("options must be an object",q.ERR_BAD_OPTION_VALUE);let n=Object.keys(e),i=n.length;for(;i-- >0;){let o=n[i],s=t[o];if(s){let t=e[o],r=void 0===t||s(t,o,e);if(!0!==r)throw new q("option "+o+" must be "+r,q.ERR_BAD_OPTION_VALUE);continue}if(!0!==r)throw new q("Unknown option "+o,q.ERR_BAD_OPTION)}},validators:ek};let eq=eI.validators;/**
 * Create a new instance of Axios
 *
 * @param {Object} instanceConfig The default config for the instance
 *
 * @return {Axios} A new instance of Axios
 */class eM{constructor(e){this.defaults=e,this.interceptors={request:new et,response:new et}}/**
   * Dispatch a request
   *
   * @param {String|Object} configOrUrl The config specific for this request (merged with this.defaults)
   * @param {?Object} config
   *
   * @returns {Promise} The Promise to be fulfilled
   */request(e,t){let r,n;"string"==typeof e?(t=t||{}).url=e:t=e||{},t=eD(this.defaults,t);let{transitional:i,paramsSerializer:o,headers:s}=t;void 0!==i&&eI.assertOptions(i,{silentJSONParsing:eq.transitional(eq.boolean),forcedJSONParsing:eq.transitional(eq.boolean),clarifyTimeoutError:eq.transitional(eq.boolean)},!1),null!=o&&(I.isFunction(o)?t.paramsSerializer={serialize:o}:eI.assertOptions(o,{encode:eq.function,serialize:eq.function},!0)),// Set config.method
t.method=(t.method||this.defaults.method||"get").toLowerCase();// Flatten headers
let a=s&&I.merge(s.common,s[t.method]);s&&I.forEach(["delete","get","head","post","put","patch","common"],e=>{delete s[e]}),t.headers=eb.concat(a,s);// filter out skipped interceptors
let l=[],u=!0;this.interceptors.request.forEach(function(e){("function"!=typeof e.runWhen||!1!==e.runWhen(t))&&(u=u&&e.synchronous,l.unshift(e.fulfilled,e.rejected))});let c=[];this.interceptors.response.forEach(function(e){c.push(e.fulfilled,e.rejected)});let d=0;if(!u){let e=[eF.bind(this),void 0];for(e.unshift.apply(e,l),e.push.apply(e,c),n=e.length,r=Promise.resolve(t);d<n;)r=r.then(e[d++],e[d++]);return r}n=l.length;let f=t;for(d=0;d<n;){let e=l[d++],t=l[d++];try{f=e(f)}catch(e){t.call(this,e);break}}try{r=eF.call(this,f)}catch(e){return Promise.reject(e)}for(d=0,n=c.length;d<n;)r=r.then(c[d++],c[d++]);return r}getUri(e){e=eD(this.defaults,e);let t=ev(e.baseURL,e.url);return ee(t,e.params,e.paramsSerializer)}}I.forEach(["delete","get","head","options"],function(e){/*eslint func-names:0*/eM.prototype[e]=function(t,r){return this.request(eD(r||{},{method:e,url:t,data:(r||{}).data}))}}),I.forEach(["post","put","patch"],function(e){/*eslint func-names:0*/function t(t){return function(r,n,i){return this.request(eD(i||{},{method:e,headers:t?{"Content-Type":"multipart/form-data"}:{},url:r,data:n}))}}eM.prototype[e]=t(),eM.prototype[e+"Form"]=t(!0)});/**
 * A `CancelToken` is an object that can be used to request cancellation of an operation.
 *
 * @param {Function} executor The executor function.
 *
 * @returns {CancelToken}
 */class eH{constructor(e){let t;if("function"!=typeof e)throw TypeError("executor must be a function.");this.promise=new Promise(function(e){t=e});let r=this;// eslint-disable-next-line func-names
this.promise.then(e=>{if(!r._listeners)return;let t=r._listeners.length;for(;t-- >0;)r._listeners[t](e);r._listeners=null}),// eslint-disable-next-line func-names
this.promise.then=e=>{let t;// eslint-disable-next-line func-names
let n=new Promise(e=>{r.subscribe(e),t=e}).then(e);return n.cancel=function(){r.unsubscribe(t)},n},e(function(e,n,i){r.reason||(r.reason=new eO(e,n,i),t(r.reason))})}/**
   * Throws a `CanceledError` if cancellation has been requested.
   */throwIfRequested(){if(this.reason)throw this.reason}/**
   * Subscribe to the cancel signal
   */subscribe(e){if(this.reason){e(this.reason);return}this._listeners?this._listeners.push(e):this._listeners=[e]}/**
   * Unsubscribe from the cancel signal
   */unsubscribe(e){if(!this._listeners)return;let t=this._listeners.indexOf(e);-1!==t&&this._listeners.splice(t,1)}/**
   * Returns an object that contains a new `CancelToken` and a function that, when called,
   * cancels the `CancelToken`.
   */static source(){let e;let t=new eH(function(t){e=t});return{token:t,cancel:e}}}let eJ={Continue:100,SwitchingProtocols:101,Processing:102,EarlyHints:103,Ok:200,Created:201,Accepted:202,NonAuthoritativeInformation:203,NoContent:204,ResetContent:205,PartialContent:206,MultiStatus:207,AlreadyReported:208,ImUsed:226,MultipleChoices:300,MovedPermanently:301,Found:302,SeeOther:303,NotModified:304,UseProxy:305,Unused:306,TemporaryRedirect:307,PermanentRedirect:308,BadRequest:400,Unauthorized:401,PaymentRequired:402,Forbidden:403,NotFound:404,MethodNotAllowed:405,NotAcceptable:406,ProxyAuthenticationRequired:407,RequestTimeout:408,Conflict:409,Gone:410,LengthRequired:411,PreconditionFailed:412,PayloadTooLarge:413,UriTooLong:414,UnsupportedMediaType:415,RangeNotSatisfiable:416,ExpectationFailed:417,ImATeapot:418,MisdirectedRequest:421,UnprocessableEntity:422,Locked:423,FailedDependency:424,TooEarly:425,UpgradeRequired:426,PreconditionRequired:428,TooManyRequests:429,RequestHeaderFieldsTooLarge:431,UnavailableForLegalReasons:451,InternalServerError:500,NotImplemented:501,BadGateway:502,ServiceUnavailable:503,GatewayTimeout:504,HttpVersionNotSupported:505,VariantAlsoNegotiates:506,InsufficientStorage:507,LoopDetected:508,NotExtended:510,NetworkAuthenticationRequired:511};Object.entries(eJ).forEach(([e,t])=>{eJ[t]=e});// Create the default instance to be exported
let e$=/**
 * Create an instance of Axios
 *
 * @param {Object} defaultConfig The default config for the instance
 *
 * @returns {Axios} A new instance of Axios
 */function e(t){let r=new eM(t),n=l(eM.prototype.request,r);return I.extend(n,eM.prototype,r,{allOwnKeys:!0}),I.extend(n,r,null,{allOwnKeys:!0}),// Factory for creating new instances
n.create=function(r){return e(eD(t,r))},n}(ec);// Expose Axios class to allow class inheritance
e$.Axios=eM,// Expose Cancel & CancelToken
e$.CanceledError=eO,e$.CancelToken=eH,e$.isCancel=ew,e$.VERSION=eB,e$.toFormData=G,// Expose AxiosError class
e$.AxiosError=q,// alias for CanceledError for backward compatibility
e$.Cancel=e$.CanceledError,// Expose all/spread
e$.all=function(e){return Promise.all(e)},e$.spread=function(e){return function(t){return e.apply(null,t)}},// Expose isAxiosError
e$.isAxiosError=function(e){return I.isObject(e)&&!0===e.isAxiosError},// Expose mergeConfig
e$.mergeConfig=eD,e$.AxiosHeaders=eb,e$.formToJSON=e=>eu(I.isHTMLForm(e)?new FormData(e):e),e$.getAdapter=e_.getAdapter,e$.HttpStatusCode=eJ,e$.default=e$;// This module is intended to unwrap Axios default export as named.
// Keep top-level export same with static properties
// so that it can keep same with es module or cjs
let{Axios:eW,AxiosError:eV,CanceledError:eK,isCancel:eG,CancelToken:eX,VERSION:eQ,all:eZ,Cancel:eY,isAxiosError:e0,spread:e1,toFormData:e2,AxiosHeaders:e4,HttpStatusCode:e3,formToJSON:e5,getAdapter:e8,mergeConfig:e6}=e$;(n=o||(o={}))[n.Aborted=0]="Aborted",n[n.Successful=1]="Successful",n[n.Error=2]="Error",(i=s||(s={}))[i.Initializing=0]="Initializing",i[i.Sending=1]="Sending",i[i.Finalizing=2]="Finalizing",i[i.Done=3]="Done";class e7{/**
     * Create an S3FileFieldClient instance.
     *
     * @param options {S3FileFieldClientOptions} - A Object with all arguments.
     * @param options.baseUrl - The absolute URL to the Django server.
     * @param [options.apiConfig] - An axios configuration to use for Django API requests.
     *                              Can be extracted from an existing axios instance via `.defaults`.
     */constructor({baseUrl:e,apiConfig:t={}}){this.api=e$.create(Object.assign(Object.assign({},t),{// Add a trailing slash
baseURL:e.replace(/\/?$/,"/")}))}/**
     * Initializes an upload.
     *
     * @param file - The file to upload.
     * @param fieldId - The Django field identifier.
     */async initializeUpload(e,t){let r=await this.api.post("upload-initialize/",{field_id:t,file_name:e.name,file_size:e.size,// An unknown type is ''
content_type:e.type||"application/octet-stream"});return r.data}/**
     * Uploads all the parts in a file directly to an object store in serial.
     *
     * @param file - The file to upload.
     * @param parts - The list of parts describing how to break up the file.
     * @param onProgress - A callback for upload progress.
     */async uploadParts(e,t,r){let n=[],i=0;for(let o of t){let t=e.slice(i,i+o.size),a=await e$.put(o.upload_url,t,{// eslint-disable-next-line @typescript-eslint/no-loop-func
onUploadProgress:t=>{r({uploaded:i+t.loaded,total:e.size,state:s.Sending})}}),{etag:l}=a.headers;// ETag might be absent due to CORS misconfiguration, but dumb typings from Axios also make it
// structurally possible to be many other types
if("string"!=typeof l)throw Error("ETag header missing from response.");n.push({part_number:o.part_number,size:o.size,etag:l}),i+=o.size}return n}/**
     * Completes an upload.
     *
     * The object will exist in the object store after completion.
     *
     * @param multipartInfo - The information describing the multipart upload.
     * @param parts - The parts that were uploaded.
     */async completeUpload(e,t){let r=await this.api.post("upload-complete/",{upload_signature:e.upload_signature,upload_id:e.upload_id,parts:t}),{complete_url:n,body:i}=r.data;// Send the CompleteMultipartUpload operation to S3
await e$.post(n,i,{headers:{// By default, Axios sets "Content-Type: application/x-www-form-urlencoded" on POST
// requests. This causes AWS's API to interpret the request body as additional parameters
// to include in the signature validation, causing it to fail.
// So, do not send this request with any Content-Type, as that is what's specified by the
// CompleteMultipartUpload docs.
// Unsetting default headers via "transformRequest" is awkward (since the headers aren't
// flattened), so this is actually; the most straightforward way; the null value is passed
// through to XMLHttpRequest, then ignored.
"Content-Type":null}})}/**
     * Finalizes an upload.
     *
     * This will only succeed if the object is already present in the object store.
     *
     * @param multipartInfo - Signed information returned from /upload-complete/.
     */async finalize(e){let t=await this.api.post("finalize/",{upload_signature:e.upload_signature});return t.data.field_value}/**
     * Uploads a file using multipart upload.
     *
     * @param file - The file to upload.
     * @param fieldId - The Django field identifier.
     * @param [onProgress] - A callback for upload progress.
     */async uploadFile(e,t,r=()=>{}){r({state:s.Initializing});let n=await this.initializeUpload(e,t);r({state:s.Sending,uploaded:0,total:e.size});let i=await this.uploadParts(e,n.parts,r);r({state:s.Finalizing}),await this.completeUpload(n,i);let a=await this.finalize(n);return r({state:s.Done}),{value:a,state:o.Successful}}}function e9(e){return`s3fileinput-${e}`}class te{constructor(e){this.input=e;let t=this.input.dataset?.s3fileinput;if(!t)throw Error('Missing "data-s3fileinput" attribute on input element.');this.baseUrl=t;let r=this.input.dataset?.fieldId;if(!r)throw Error('Missing "data-field-id" attribute on input element.');this.fieldId=r,this.node=e.ownerDocument.createElement("div"),this.node.classList.add(e9("wrapper")),this.node.innerHTML=`<div class="${e9("inner")}">
    <div class="${e9("info")}"></div>
    <button type="button" class="${e9("clear")}" title="Clear (file was already uploaded tho)">
      x
    </button>
    <div class="${e9("spinner-wrapper")}">
      <div class="${e9("spinner")}"><div></div><div></div><div></div><div></div>
    </div>
  </div>`,/* eslint-disable @typescript-eslint/no-non-null-assertion */this.input.parentElement.replaceChild(this.node,this.input),// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
this.clearButton=this.node.querySelector(`.${e9("clear")}`),this.info=this.node.querySelector(`.${e9("info")}`),this.clearButton.insertAdjacentElement("beforebegin",this.input),this.spinnerWrapper=this.node.querySelector(`.${e9("spinner-wrapper")}`),/* eslint-enable @typescript-eslint/no-non-null-assertion */this.input.onchange=async e=>{e.preventDefault(),"file"===this.input.type?await this.uploadFiles():""===this.input.value&&(// already processed but user resetted it -> convert bak
this.input.type="file",this.info.innerText="",this.node.classList.remove(e9("set")))},this.clearButton.onclick=e=>{e.preventDefault(),e.stopPropagation(),this.input.type="file",this.input.value="",this.info.innerText="",this.node.classList.remove(e9("set"))}}async uploadFile(e){let t=new CustomEvent("s3UploadStarted",{detail:e});this.input.dispatchEvent(t);let r=await new e7({baseUrl:this.baseUrl,apiConfig:{// This will cause session and CSRF cookies to be sent for same-site requests.
// Cross-site requests with the server-rendered widget are not supported.
// If the server does not enable SessionAuthentication, requests will be unauthenticated,
// but still allowed.
xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFToken",// Explicitly disable this, to ensure that cross-site requests fail cleanly.
withCredentials:!1}}).uploadFile(e,this.fieldId),n=new CustomEvent("s3UploadComplete",{detail:r});return this.input.dispatchEvent(n),r}async uploadFiles(){let e=Array.from(this.input.files||[]);if(0===e.length)return;let t=this.input.getBoundingClientRect();this.spinnerWrapper.style.width=`${t.width}px`,this.spinnerWrapper.style.height=`${t.height}px`,this.node.classList.add(e9("uploading")),this.input.setCustomValidity("Uploading files, wait till finished"),this.input.value="";let r=e[0],n=await this.uploadFile(r);this.node.classList.remove(e9("uploading")),n.state===o.Successful&&(this.node.classList.add(e9("set")),this.input.setCustomValidity(""),this.input.type="hidden",this.input.value=n.value,this.info.innerText=r.name)}}function tt(){document.querySelectorAll("input[data-s3fileinput]").forEach(e=>{// eslint-disable-next-line no-new
new te(e)})}"loading"!==document.readyState?tt():document.addEventListener("DOMContentLoaded",tt.bind(void 0))})();