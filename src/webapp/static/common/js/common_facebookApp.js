/*!
 * jQuery JavaScript Library v1.5.1
 * http://jquery.com/
 *
 * Copyright 2011, John Resig
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * Includes Sizzle.js
 * http://sizzlejs.com/
 * Copyright 2011, The Dojo Foundation
 * Released under the MIT, BSD, and GPL Licenses.
 *
 * Date: Wed Feb 23 13:55:29 2011 -0500
 */
(function(a,b){function cg(a){return d.isWindow(a)?a:a.nodeType===9?a.defaultView||a.parentWindow:!1}function cd(a){if(!bZ[a]){var b=d("<"+a+">").appendTo("body"),c=b.css("display");b.remove();if(c==="none"||c==="")c="block";bZ[a]=c}return bZ[a]}function cc(a,b){var c={};d.each(cb.concat.apply([],cb.slice(0,b)),function(){c[this]=a});return c}function bY(){try{return new a.ActiveXObject("Microsoft.XMLHTTP")}catch(b){}}function bX(){try{return new a.XMLHttpRequest}catch(b){}}function bW(){d(a).unload(function(){for(var a in bU)bU[a](0,1)})}function bQ(a,c){a.dataFilter&&(c=a.dataFilter(c,a.dataType));var e=a.dataTypes,f={},g,h,i=e.length,j,k=e[0],l,m,n,o,p;for(g=1;g<i;g++){if(g===1)for(h in a.converters)typeof h==="string"&&(f[h.toLowerCase()]=a.converters[h]);l=k,k=e[g];if(k==="*")k=l;else if(l!=="*"&&l!==k){m=l+" "+k,n=f[m]||f["* "+k];if(!n){p=b;for(o in f){j=o.split(" ");if(j[0]===l||j[0]==="*"){p=f[j[1]+" "+k];if(p){o=f[o],o===!0?n=p:p===!0&&(n=o);break}}}}!n&&!p&&d.error("No conversion from "+m.replace(" "," to ")),n!==!0&&(c=n?n(c):p(o(c)))}}return c}function bP(a,c,d){var e=a.contents,f=a.dataTypes,g=a.responseFields,h,i,j,k;for(i in g)i in d&&(c[g[i]]=d[i]);while(f[0]==="*")f.shift(),h===b&&(h=a.mimeType||c.getResponseHeader("content-type"));if(h)for(i in e)if(e[i]&&e[i].test(h)){f.unshift(i);break}if(f[0]in d)j=f[0];else{for(i in d){if(!f[0]||a.converters[i+" "+f[0]]){j=i;break}k||(k=i)}j=j||k}if(j){j!==f[0]&&f.unshift(j);return d[j]}}function bO(a,b,c,e){if(d.isArray(b)&&b.length)d.each(b,function(b,f){c||bq.test(a)?e(a,f):bO(a+"["+(typeof f==="object"||d.isArray(f)?b:"")+"]",f,c,e)});else if(c||b==null||typeof b!=="object")e(a,b);else if(d.isArray(b)||d.isEmptyObject(b))e(a,"");else for(var f in b)bO(a+"["+f+"]",b[f],c,e)}function bN(a,c,d,e,f,g){f=f||c.dataTypes[0],g=g||{},g[f]=!0;var h=a[f],i=0,j=h?h.length:0,k=a===bH,l;for(;i<j&&(k||!l);i++)l=h[i](c,d,e),typeof l==="string"&&(!k||g[l]?l=b:(c.dataTypes.unshift(l),l=bN(a,c,d,e,l,g)));(k||!l)&&!g["*"]&&(l=bN(a,c,d,e,"*",g));return l}function bM(a){return function(b,c){typeof b!=="string"&&(c=b,b="*");if(d.isFunction(c)){var e=b.toLowerCase().split(bB),f=0,g=e.length,h,i,j;for(;f<g;f++)h=e[f],j=/^\+/.test(h),j&&(h=h.substr(1)||"*"),i=a[h]=a[h]||[],i[j?"unshift":"push"](c)}}}function bo(a,b,c){var e=b==="width"?bi:bj,f=b==="width"?a.offsetWidth:a.offsetHeight;if(c==="border")return f;d.each(e,function(){c||(f-=parseFloat(d.css(a,"padding"+this))||0),c==="margin"?f+=parseFloat(d.css(a,"margin"+this))||0:f-=parseFloat(d.css(a,"border"+this+"Width"))||0});return f}function ba(a,b){b.src?d.ajax({url:b.src,async:!1,dataType:"script"}):d.globalEval(b.text||b.textContent||b.innerHTML||""),b.parentNode&&b.parentNode.removeChild(b)}function _(a){return"getElementsByTagName"in a?a.getElementsByTagName("*"):"querySelectorAll"in a?a.querySelectorAll("*"):[]}function $(a,b){if(b.nodeType===1){var c=b.nodeName.toLowerCase();b.clearAttributes(),b.mergeAttributes(a);if(c==="object")b.outerHTML=a.outerHTML;else if(c!=="input"||a.type!=="checkbox"&&a.type!=="radio"){if(c==="option")b.selected=a.defaultSelected;else if(c==="input"||c==="textarea")b.defaultValue=a.defaultValue}else a.checked&&(b.defaultChecked=b.checked=a.checked),b.value!==a.value&&(b.value=a.value);b.removeAttribute(d.expando)}}function Z(a,b){if(b.nodeType===1&&d.hasData(a)){var c=d.expando,e=d.data(a),f=d.data(b,e);if(e=e[c]){var g=e.events;f=f[c]=d.extend({},e);if(g){delete f.handle,f.events={};for(var h in g)for(var i=0,j=g[h].length;i<j;i++)d.event.add(b,h+(g[h][i].namespace?".":"")+g[h][i].namespace,g[h][i],g[h][i].data)}}}}function Y(a,b){return d.nodeName(a,"table")?a.getElementsByTagName("tbody")[0]||a.appendChild(a.ownerDocument.createElement("tbody")):a}function O(a,b,c){if(d.isFunction(b))return d.grep(a,function(a,d){var e=!!b.call(a,d,a);return e===c});if(b.nodeType)return d.grep(a,function(a,d){return a===b===c});if(typeof b==="string"){var e=d.grep(a,function(a){return a.nodeType===1});if(J.test(b))return d.filter(b,e,!c);b=d.filter(b,e)}return d.grep(a,function(a,e){return d.inArray(a,b)>=0===c})}function N(a){return!a||!a.parentNode||a.parentNode.nodeType===11}function F(a,b){return(a&&a!=="*"?a+".":"")+b.replace(r,"`").replace(s,"&")}function E(a){var b,c,e,f,g,h,i,j,k,l,m,n,o,q=[],r=[],s=d._data(this,"events");if(a.liveFired!==this&&s&&s.live&&!a.target.disabled&&(!a.button||a.type!=="click")){a.namespace&&(n=new RegExp("(^|\\.)"+a.namespace.split(".").join("\\.(?:.*\\.)?")+"(\\.|$)")),a.liveFired=this;var t=s.live.slice(0);for(i=0;i<t.length;i++)g=t[i],g.origType.replace(p,"")===a.type?r.push(g.selector):t.splice(i--,1);f=d(a.target).closest(r,a.currentTarget);for(j=0,k=f.length;j<k;j++){m=f[j];for(i=0;i<t.length;i++){g=t[i];if(m.selector===g.selector&&(!n||n.test(g.namespace))&&!m.elem.disabled){h=m.elem,e=null;if(g.preType==="mouseenter"||g.preType==="mouseleave")a.type=g.preType,e=d(a.relatedTarget).closest(g.selector)[0];(!e||e!==h)&&q.push({elem:h,handleObj:g,level:m.level})}}}for(j=0,k=q.length;j<k;j++){f=q[j];if(c&&f.level>c)break;a.currentTarget=f.elem,a.data=f.handleObj.data,a.handleObj=f.handleObj,o=f.handleObj.origHandler.apply(f.elem,arguments);if(o===!1||a.isPropagationStopped()){c=f.level,o===!1&&(b=!1);if(a.isImmediatePropagationStopped())break}}return b}}function C(a,c,e){var f=d.extend({},e[0]);f.type=a,f.originalEvent={},f.liveFired=b,d.event.handle.call(c,f),f.isDefaultPrevented()&&e[0].preventDefault()}function w(){return!0}function v(){return!1}function g(a){for(var b in a)if(b!=="toJSON")return!1;return!0}function f(a,c,f){if(f===b&&a.nodeType===1){f=a.getAttribute("data-"+c);if(typeof f==="string"){try{f=f==="true"?!0:f==="false"?!1:f==="null"?null:d.isNaN(f)?e.test(f)?d.parseJSON(f):f:parseFloat(f)}catch(g){}d.data(a,c,f)}else f=b}return f}var c=a.document,d=function(){function I(){if(!d.isReady){try{c.documentElement.doScroll("left")}catch(a){setTimeout(I,1);return}d.ready()}}var d=function(a,b){return new d.fn.init(a,b,g)},e=a.jQuery,f=a.$,g,h=/^(?:[^<]*(<[\w\W]+>)[^>]*$|#([\w\-]+)$)/,i=/\S/,j=/^\s+/,k=/\s+$/,l=/\d/,m=/^<(\w+)\s*\/?>(?:<\/\1>)?$/,n=/^[\],:{}\s]*$/,o=/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,p=/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,q=/(?:^|:|,)(?:\s*\[)+/g,r=/(webkit)[ \/]([\w.]+)/,s=/(opera)(?:.*version)?[ \/]([\w.]+)/,t=/(msie) ([\w.]+)/,u=/(mozilla)(?:.*? rv:([\w.]+))?/,v=navigator.userAgent,w,x=!1,y,z="then done fail isResolved isRejected promise".split(" "),A,B=Object.prototype.toString,C=Object.prototype.hasOwnProperty,D=Array.prototype.push,E=Array.prototype.slice,F=String.prototype.trim,G=Array.prototype.indexOf,H={};d.fn=d.prototype={constructor:d,init:function(a,e,f){var g,i,j,k;if(!a)return this;if(a.nodeType){this.context=this[0]=a,this.length=1;return this}if(a==="body"&&!e&&c.body){this.context=c,this[0]=c.body,this.selector="body",this.length=1;return this}if(typeof a==="string"){g=h.exec(a);if(!g||!g[1]&&e)return!e||e.jquery?(e||f).find(a):this.constructor(e).find(a);if(g[1]){e=e instanceof d?e[0]:e,k=e?e.ownerDocument||e:c,j=m.exec(a),j?d.isPlainObject(e)?(a=[c.createElement(j[1])],d.fn.attr.call(a,e,!0)):a=[k.createElement(j[1])]:(j=d.buildFragment([g[1]],[k]),a=(j.cacheable?d.clone(j.fragment):j.fragment).childNodes);return d.merge(this,a)}i=c.getElementById(g[2]);if(i&&i.parentNode){if(i.id!==g[2])return f.find(a);this.length=1,this[0]=i}this.context=c,this.selector=a;return this}if(d.isFunction(a))return f.ready(a);a.selector!==b&&(this.selector=a.selector,this.context=a.context);return d.makeArray(a,this)},selector:"",jquery:"1.5.1",length:0,size:function(){return this.length},toArray:function(){return E.call(this,0)},get:function(a){return a==null?this.toArray():a<0?this[this.length+a]:this[a]},pushStack:function(a,b,c){var e=this.constructor();d.isArray(a)?D.apply(e,a):d.merge(e,a),e.prevObject=this,e.context=this.context,b==="find"?e.selector=this.selector+(this.selector?" ":"")+c:b&&(e.selector=this.selector+"."+b+"("+c+")");return e},each:function(a,b){return d.each(this,a,b)},ready:function(a){d.bindReady(),y.done(a);return this},eq:function(a){return a===-1?this.slice(a):this.slice(a,+a+1)},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},slice:function(){return this.pushStack(E.apply(this,arguments),"slice",E.call(arguments).join(","))},map:function(a){return this.pushStack(d.map(this,function(b,c){return a.call(b,c,b)}))},end:function(){return this.prevObject||this.constructor(null)},push:D,sort:[].sort,splice:[].splice},d.fn.init.prototype=d.fn,d.extend=d.fn.extend=function(){var a,c,e,f,g,h,i=arguments[0]||{},j=1,k=arguments.length,l=!1;typeof i==="boolean"&&(l=i,i=arguments[1]||{},j=2),typeof i!=="object"&&!d.isFunction(i)&&(i={}),k===j&&(i=this,--j);for(;j<k;j++)if((a=arguments[j])!=null)for(c in a){e=i[c],f=a[c];if(i===f)continue;l&&f&&(d.isPlainObject(f)||(g=d.isArray(f)))?(g?(g=!1,h=e&&d.isArray(e)?e:[]):h=e&&d.isPlainObject(e)?e:{},i[c]=d.extend(l,h,f)):f!==b&&(i[c]=f)}return i},d.extend({noConflict:function(b){a.$=f,b&&(a.jQuery=e);return d},isReady:!1,readyWait:1,ready:function(a){a===!0&&d.readyWait--;if(!d.readyWait||a!==!0&&!d.isReady){if(!c.body)return setTimeout(d.ready,1);d.isReady=!0;if(a!==!0&&--d.readyWait>0)return;y.resolveWith(c,[d]),d.fn.trigger&&d(c).trigger("ready").unbind("ready")}},bindReady:function(){if(!x){x=!0;if(c.readyState==="complete")return setTimeout(d.ready,1);if(c.addEventListener)c.addEventListener("DOMContentLoaded",A,!1),a.addEventListener("load",d.ready,!1);else if(c.attachEvent){c.attachEvent("onreadystatechange",A),a.attachEvent("onload",d.ready);var b=!1;try{b=a.frameElement==null}catch(e){}c.documentElement.doScroll&&b&&I()}}},isFunction:function(a){return d.type(a)==="function"},isArray:Array.isArray||function(a){return d.type(a)==="array"},isWindow:function(a){return a&&typeof a==="object"&&"setInterval"in a},isNaN:function(a){return a==null||!l.test(a)||isNaN(a)},type:function(a){return a==null?String(a):H[B.call(a)]||"object"},isPlainObject:function(a){if(!a||d.type(a)!=="object"||a.nodeType||d.isWindow(a))return!1;if(a.constructor&&!C.call(a,"constructor")&&!C.call(a.constructor.prototype,"isPrototypeOf"))return!1;var c;for(c in a){}return c===b||C.call(a,c)},isEmptyObject:function(a){for(var b in a)return!1;return!0},error:function(a){throw a},parseJSON:function(b){if(typeof b!=="string"||!b)return null;b=d.trim(b);if(n.test(b.replace(o,"@").replace(p,"]").replace(q,"")))return a.JSON&&a.JSON.parse?a.JSON.parse(b):(new Function("return "+b))();d.error("Invalid JSON: "+b)},parseXML:function(b,c,e){a.DOMParser?(e=new DOMParser,c=e.parseFromString(b,"text/xml")):(c=new ActiveXObject("Microsoft.XMLDOM"),c.async="false",c.loadXML(b)),e=c.documentElement,(!e||!e.nodeName||e.nodeName==="parsererror")&&d.error("Invalid XML: "+b);return c},noop:function(){},globalEval:function(a){if(a&&i.test(a)){var b=c.head||c.getElementsByTagName("head")[0]||c.documentElement,e=c.createElement("script");d.support.scriptEval()?e.appendChild(c.createTextNode(a)):e.text=a,b.insertBefore(e,b.firstChild),b.removeChild(e)}},nodeName:function(a,b){return a.nodeName&&a.nodeName.toUpperCase()===b.toUpperCase()},each:function(a,c,e){var f,g=0,h=a.length,i=h===b||d.isFunction(a);if(e){if(i){for(f in a)if(c.apply(a[f],e)===!1)break}else for(;g<h;)if(c.apply(a[g++],e)===!1)break}else if(i){for(f in a)if(c.call(a[f],f,a[f])===!1)break}else for(var j=a[0];g<h&&c.call(j,g,j)!==!1;j=a[++g]){}return a},trim:F?function(a){return a==null?"":F.call(a)}:function(a){return a==null?"":(a+"").replace(j,"").replace(k,"")},makeArray:function(a,b){var c=b||[];if(a!=null){var e=d.type(a);a.length==null||e==="string"||e==="function"||e==="regexp"||d.isWindow(a)?D.call(c,a):d.merge(c,a)}return c},inArray:function(a,b){if(b.indexOf)return b.indexOf(a);for(var c=0,d=b.length;c<d;c++)if(b[c]===a)return c;return-1},merge:function(a,c){var d=a.length,e=0;if(typeof c.length==="number")for(var f=c.length;e<f;e++)a[d++]=c[e];else while(c[e]!==b)a[d++]=c[e++];a.length=d;return a},grep:function(a,b,c){var d=[],e;c=!!c;for(var f=0,g=a.length;f<g;f++)e=!!b(a[f],f),c!==e&&d.push(a[f]);return d},map:function(a,b,c){var d=[],e;for(var f=0,g=a.length;f<g;f++)e=b(a[f],f,c),e!=null&&(d[d.length]=e);return d.concat.apply([],d)},guid:1,proxy:function(a,c,e){arguments.length===2&&(typeof c==="string"?(e=a,a=e[c],c=b):c&&!d.isFunction(c)&&(e=c,c=b)),!c&&a&&(c=function(){return a.apply(e||this,arguments)}),a&&(c.guid=a.guid=a.guid||c.guid||d.guid++);return c},access:function(a,c,e,f,g,h){var i=a.length;if(typeof c==="object"){for(var j in c)d.access(a,j,c[j],f,g,e);return a}if(e!==b){f=!h&&f&&d.isFunction(e);for(var k=0;k<i;k++)g(a[k],c,f?e.call(a[k],k,g(a[k],c)):e,h);return a}return i?g(a[0],c):b},now:function(){return(new Date).getTime()},_Deferred:function(){var a=[],b,c,e,f={done:function(){if(!e){var c=arguments,g,h,i,j,k;b&&(k=b,b=0);for(g=0,h=c.length;g<h;g++)i=c[g],j=d.type(i),j==="array"?f.done.apply(f,i):j==="function"&&a.push(i);k&&f.resolveWith(k[0],k[1])}return this},resolveWith:function(d,f){if(!e&&!b&&!c){c=1;try{while(a[0])a.shift().apply(d,f)}catch(g){throw g}finally{b=[d,f],c=0}}return this},resolve:function(){f.resolveWith(d.isFunction(this.promise)?this.promise():this,arguments);return this},isResolved:function(){return c||b},cancel:function(){e=1,a=[];return this}};return f},Deferred:function(a){var b=d._Deferred(),c=d._Deferred(),e;d.extend(b,{then:function(a,c){b.done(a).fail(c);return this},fail:c.done,rejectWith:c.resolveWith,reject:c.resolve,isRejected:c.isResolved,promise:function(a){if(a==null){if(e)return e;e=a={}}var c=z.length;while(c--)a[z[c]]=b[z[c]];return a}}),b.done(c.cancel).fail(b.cancel),delete b.cancel,a&&a.call(b,b);return b},when:function(a){var b=arguments.length,c=b<=1&&a&&d.isFunction(a.promise)?a:d.Deferred(),e=c.promise();if(b>1){var f=E.call(arguments,0),g=b,h=function(a){return function(b){f[a]=arguments.length>1?E.call(arguments,0):b,--g||c.resolveWith(e,f)}};while(b--)a=f[b],a&&d.isFunction(a.promise)?a.promise().then(h(b),c.reject):--g;g||c.resolveWith(e,f)}else c!==a&&c.resolve(a);return e},uaMatch:function(a){a=a.toLowerCase();var b=r.exec(a)||s.exec(a)||t.exec(a)||a.indexOf("compatible")<0&&u.exec(a)||[];return{browser:b[1]||"",version:b[2]||"0"}},sub:function(){function a(b,c){return new a.fn.init(b,c)}d.extend(!0,a,this),a.superclass=this,a.fn=a.prototype=this(),a.fn.constructor=a,a.subclass=this.subclass,a.fn.init=function b(b,c){c&&c instanceof d&&!(c instanceof a)&&(c=a(c));return d.fn.init.call(this,b,c,e)},a.fn.init.prototype=a.fn;var e=a(c);return a},browser:{}}),y=d._Deferred(),d.each("Boolean Number String Function Array Date RegExp Object".split(" "),function(a,b){H["[object "+b+"]"]=b.toLowerCase()}),w=d.uaMatch(v),w.browser&&(d.browser[w.browser]=!0,d.browser.version=w.version),d.browser.webkit&&(d.browser.safari=!0),G&&(d.inArray=function(a,b){return G.call(b,a)}),i.test(" ")&&(j=/^[\s\xA0]+/,k=/[\s\xA0]+$/),g=d(c),c.addEventListener?A=function(){c.removeEventListener("DOMContentLoaded",A,!1),d.ready()}:c.attachEvent&&(A=function(){c.readyState==="complete"&&(c.detachEvent("onreadystatechange",A),d.ready())});return d}();(function(){d.support={};var b=c.createElement("div");b.style.display="none",b.innerHTML="   <link/><table></table><a href='/a' style='color:red;float:left;opacity:.55;'>a</a><input type='checkbox'/>";var e=b.getElementsByTagName("*"),f=b.getElementsByTagName("a")[0],g=c.createElement("select"),h=g.appendChild(c.createElement("option")),i=b.getElementsByTagName("input")[0];if(e&&e.length&&f){d.support={leadingWhitespace:b.firstChild.nodeType===3,tbody:!b.getElementsByTagName("tbody").length,htmlSerialize:!!b.getElementsByTagName("link").length,style:/red/.test(f.getAttribute("style")),hrefNormalized:f.getAttribute("href")==="/a",opacity:/^0.55$/.test(f.style.opacity),cssFloat:!!f.style.cssFloat,checkOn:i.value==="on",optSelected:h.selected,deleteExpando:!0,optDisabled:!1,checkClone:!1,noCloneEvent:!0,noCloneChecked:!0,boxModel:null,inlineBlockNeedsLayout:!1,shrinkWrapBlocks:!1,reliableHiddenOffsets:!0},i.checked=!0,d.support.noCloneChecked=i.cloneNode(!0).checked,g.disabled=!0,d.support.optDisabled=!h.disabled;var j=null;d.support.scriptEval=function(){if(j===null){var b=c.documentElement,e=c.createElement("script"),f="script"+d.now();try{e.appendChild(c.createTextNode("window."+f+"=1;"))}catch(g){}b.insertBefore(e,b.firstChild),a[f]?(j=!0,delete a[f]):j=!1,b.removeChild(e),b=e=f=null}return j};try{delete b.test}catch(k){d.support.deleteExpando=!1}!b.addEventListener&&b.attachEvent&&b.fireEvent&&(b.attachEvent("onclick",function l(){d.support.noCloneEvent=!1,b.detachEvent("onclick",l)}),b.cloneNode(!0).fireEvent("onclick")),b=c.createElement("div"),b.innerHTML="<input type='radio' name='radiotest' checked='checked'/>";var m=c.createDocumentFragment();m.appendChild(b.firstChild),d.support.checkClone=m.cloneNode(!0).cloneNode(!0).lastChild.checked,d(function(){var a=c.createElement("div"),b=c.getElementsByTagName("body")[0];if(b){a.style.width=a.style.paddingLeft="1px",b.appendChild(a),d.boxModel=d.support.boxModel=a.offsetWidth===2,"zoom"in a.style&&(a.style.display="inline",a.style.zoom=1,d.support.inlineBlockNeedsLayout=a.offsetWidth===2,a.style.display="",a.innerHTML="<div style='width:4px;'></div>",d.support.shrinkWrapBlocks=a.offsetWidth!==2),a.innerHTML="<table><tr><td style='padding:0;border:0;display:none'></td><td>t</td></tr></table>";var e=a.getElementsByTagName("td");d.support.reliableHiddenOffsets=e[0].offsetHeight===0,e[0].style.display="",e[1].style.display="none",d.support.reliableHiddenOffsets=d.support.reliableHiddenOffsets&&e[0].offsetHeight===0,a.innerHTML="",b.removeChild(a).style.display="none",a=e=null}});var n=function(a){var b=c.createElement("div");a="on"+a;if(!b.attachEvent)return!0;var d=a in b;d||(b.setAttribute(a,"return;"),d=typeof b[a]==="function"),b=null;return d};d.support.submitBubbles=n("submit"),d.support.changeBubbles=n("change"),b=e=f=null}})();var e=/^(?:\{.*\}|\[.*\])$/;d.extend({cache:{},uuid:0,expando:"jQuery"+(d.fn.jquery+Math.random()).replace(/\D/g,""),noData:{embed:!0,object:"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",applet:!0},hasData:function(a){a=a.nodeType?d.cache[a[d.expando]]:a[d.expando];return!!a&&!g(a)},data:function(a,c,e,f){if(d.acceptData(a)){var g=d.expando,h=typeof c==="string",i,j=a.nodeType,k=j?d.cache:a,l=j?a[d.expando]:a[d.expando]&&d.expando;if((!l||f&&l&&!k[l][g])&&h&&e===b)return;l||(j?a[d.expando]=l=++d.uuid:l=d.expando),k[l]||(k[l]={},j||(k[l].toJSON=d.noop));if(typeof c==="object"||typeof c==="function")f?k[l][g]=d.extend(k[l][g],c):k[l]=d.extend(k[l],c);i=k[l],f&&(i[g]||(i[g]={}),i=i[g]),e!==b&&(i[c]=e);if(c==="events"&&!i[c])return i[g]&&i[g].events;return h?i[c]:i}},removeData:function(b,c,e){if(d.acceptData(b)){var f=d.expando,h=b.nodeType,i=h?d.cache:b,j=h?b[d.expando]:d.expando;if(!i[j])return;if(c){var k=e?i[j][f]:i[j];if(k){delete k[c];if(!g(k))return}}if(e){delete i[j][f];if(!g(i[j]))return}var l=i[j][f];d.support.deleteExpando||i!=a?delete i[j]:i[j]=null,l?(i[j]={},h||(i[j].toJSON=d.noop),i[j][f]=l):h&&(d.support.deleteExpando?delete b[d.expando]:b.removeAttribute?b.removeAttribute(d.expando):b[d.expando]=null)}},_data:function(a,b,c){return d.data(a,b,c,!0)},acceptData:function(a){if(a.nodeName){var b=d.noData[a.nodeName.toLowerCase()];if(b)return b!==!0&&a.getAttribute("classid")===b}return!0}}),d.fn.extend({data:function(a,c){var e=null;if(typeof a==="undefined"){if(this.length){e=d.data(this[0]);if(this[0].nodeType===1){var g=this[0].attributes,h;for(var i=0,j=g.length;i<j;i++)h=g[i].name,h.indexOf("data-")===0&&(h=h.substr(5),f(this[0],h,e[h]))}}return e}if(typeof a==="object")return this.each(function(){d.data(this,a)});var k=a.split(".");k[1]=k[1]?"."+k[1]:"";if(c===b){e=this.triggerHandler("getData"+k[1]+"!",[k[0]]),e===b&&this.length&&(e=d.data(this[0],a),e=f(this[0],a,e));return e===b&&k[1]?this.data(k[0]):e}return this.each(function(){var b=d(this),e=[k[0],c];b.triggerHandler("setData"+k[1]+"!",e),d.data(this,a,c),b.triggerHandler("changeData"+k[1]+"!",e)})},removeData:function(a){return this.each(function(){d.removeData(this,a)})}}),d.extend({queue:function(a,b,c){if(a){b=(b||"fx")+"queue";var e=d._data(a,b);if(!c)return e||[];!e||d.isArray(c)?e=d._data(a,b,d.makeArray(c)):e.push(c);return e}},dequeue:function(a,b){b=b||"fx";var c=d.queue(a,b),e=c.shift();e==="inprogress"&&(e=c.shift()),e&&(b==="fx"&&c.unshift("inprogress"),e.call(a,function(){d.dequeue(a,b)})),c.length||d.removeData(a,b+"queue",!0)}}),d.fn.extend({queue:function(a,c){typeof a!=="string"&&(c=a,a="fx");if(c===b)return d.queue(this[0],a);return this.each(function(b){var e=d.queue(this,a,c);a==="fx"&&e[0]!=="inprogress"&&d.dequeue(this,a)})},dequeue:function(a){return this.each(function(){d.dequeue(this,a)})},delay:function(a,b){a=d.fx?d.fx.speeds[a]||a:a,b=b||"fx";return this.queue(b,function(){var c=this;setTimeout(function(){d.dequeue(c,b)},a)})},clearQueue:function(a){return this.queue(a||"fx",[])}});var h=/[\n\t\r]/g,i=/\s+/,j=/\r/g,k=/^(?:href|src|style)$/,l=/^(?:button|input)$/i,m=/^(?:button|input|object|select|textarea)$/i,n=/^a(?:rea)?$/i,o=/^(?:radio|checkbox)$/i;d.props={"for":"htmlFor","class":"className",readonly:"readOnly",maxlength:"maxLength",cellspacing:"cellSpacing",rowspan:"rowSpan",colspan:"colSpan",tabindex:"tabIndex",usemap:"useMap",frameborder:"frameBorder"},d.fn.extend({attr:function(a,b){return d.access(this,a,b,!0,d.attr)},removeAttr:function(a,b){return this.each(function(){d.attr(this,a,""),this.nodeType===1&&this.removeAttribute(a)})},addClass:function(a){if(d.isFunction(a))return this.each(function(b){var c=d(this);c.addClass(a.call(this,b,c.attr("class")))});if(a&&typeof a==="string"){var b=(a||"").split(i);for(var c=0,e=this.length;c<e;c++){var f=this[c];if(f.nodeType===1)if(f.className){var g=" "+f.className+" ",h=f.className;for(var j=0,k=b.length;j<k;j++)g.indexOf(" "+b[j]+" ")<0&&(h+=" "+b[j]);f.className=d.trim(h)}else f.className=a}}return this},removeClass:function(a){if(d.isFunction(a))return this.each(function(b){var c=d(this);c.removeClass(a.call(this,b,c.attr("class")))});if(a&&typeof a==="string"||a===b){var c=(a||"").split(i);for(var e=0,f=this.length;e<f;e++){var g=this[e];if(g.nodeType===1&&g.className)if(a){var j=(" "+g.className+" ").replace(h," ");for(var k=0,l=c.length;k<l;k++)j=j.replace(" "+c[k]+" "," ");g.className=d.trim(j)}else g.className=""}}return this},toggleClass:function(a,b){var c=typeof a,e=typeof b==="boolean";if(d.isFunction(a))return this.each(function(c){var e=d(this);e.toggleClass(a.call(this,c,e.attr("class"),b),b)});return this.each(function(){if(c==="string"){var f,g=0,h=d(this),j=b,k=a.split(i);while(f=k[g++])j=e?j:!h.hasClass(f),h[j?"addClass":"removeClass"](f)}else if(c==="undefined"||c==="boolean")this.className&&d._data(this,"__className__",this.className),this.className=this.className||a===!1?"":d._data(this,"__className__")||""})},hasClass:function(a){var b=" "+a+" ";for(var c=0,d=this.length;c<d;c++)if((" "+this[c].className+" ").replace(h," ").indexOf(b)>-1)return!0;return!1},val:function(a){if(!arguments.length){var c=this[0];if(c){if(d.nodeName(c,"option")){var e=c.attributes.value;return!e||e.specified?c.value:c.text}if(d.nodeName(c,"select")){var f=c.selectedIndex,g=[],h=c.options,i=c.type==="select-one";if(f<0)return null;for(var k=i?f:0,l=i?f+1:h.length;k<l;k++){var m=h[k];if(m.selected&&(d.support.optDisabled?!m.disabled:m.getAttribute("disabled")===null)&&(!m.parentNode.disabled||!d.nodeName(m.parentNode,"optgroup"))){a=d(m).val();if(i)return a;g.push(a)}}if(i&&!g.length&&h.length)return d(h[f]).val();return g}if(o.test(c.type)&&!d.support.checkOn)return c.getAttribute("value")===null?"on":c.value;return(c.value||"").replace(j,"")}return b}var n=d.isFunction(a);return this.each(function(b){var c=d(this),e=a;if(this.nodeType===1){n&&(e=a.call(this,b,c.val())),e==null?e="":typeof e==="number"?e+="":d.isArray(e)&&(e=d.map(e,function(a){return a==null?"":a+""}));if(d.isArray(e)&&o.test(this.type))this.checked=d.inArray(c.val(),e)>=0;else if(d.nodeName(this,"select")){var f=d.makeArray(e);d("option",this).each(function(){this.selected=d.inArray(d(this).val(),f)>=0}),f.length||(this.selectedIndex=-1)}else this.value=e}})}}),d.extend({attrFn:{val:!0,css:!0,html:!0,text:!0,data:!0,width:!0,height:!0,offset:!0},attr:function(a,c,e,f){if(!a||a.nodeType===3||a.nodeType===8||a.nodeType===2)return b;if(f&&c in d.attrFn)return d(a)[c](e);var g=a.nodeType!==1||!d.isXMLDoc(a),h=e!==b;c=g&&d.props[c]||c;if(a.nodeType===1){var i=k.test(c);if(c==="selected"&&!d.support.optSelected){var j=a.parentNode;j&&(j.selectedIndex,j.parentNode&&j.parentNode.selectedIndex)}if((c in a||a[c]!==b)&&g&&!i){h&&(c==="type"&&l.test(a.nodeName)&&a.parentNode&&d.error("type property can't be changed"),e===null?a.nodeType===1&&a.removeAttribute(c):a[c]=e);if(d.nodeName(a,"form")&&a.getAttributeNode(c))return a.getAttributeNode(c).nodeValue;if(c==="tabIndex"){var o=a.getAttributeNode("tabIndex");return o&&o.specified?o.value:m.test(a.nodeName)||n.test(a.nodeName)&&a.href?0:b}return a[c]}if(!d.support.style&&g&&c==="style"){h&&(a.style.cssText=""+e);return a.style.cssText}h&&a.setAttribute(c,""+e);if(!a.attributes[c]&&(a.hasAttribute&&!a.hasAttribute(c)))return b;var p=!d.support.hrefNormalized&&g&&i?a.getAttribute(c,2):a.getAttribute(c);return p===null?b:p}h&&(a[c]=e);return a[c]}});var p=/\.(.*)$/,q=/^(?:textarea|input|select)$/i,r=/\./g,s=/ /g,t=/[^\w\s.|`]/g,u=function(a){return a.replace(t,"\\$&")};d.event={add:function(c,e,f,g){if(c.nodeType!==3&&c.nodeType!==8){try{d.isWindow(c)&&(c!==a&&!c.frameElement)&&(c=a)}catch(h){}if(f===!1)f=v;else if(!f)return;var i,j;f.handler&&(i=f,f=i.handler),f.guid||(f.guid=d.guid++);var k=d._data(c);if(!k)return;var l=k.events,m=k.handle;l||(k.events=l={}),m||(k.handle=m=function(){return typeof d!=="undefined"&&!d.event.triggered?d.event.handle.apply(m.elem,arguments):b}),m.elem=c,e=e.split(" ");var n,o=0,p;while(n=e[o++]){j=i?d.extend({},i):{handler:f,data:g},n.indexOf(".")>-1?(p=n.split("."),n=p.shift(),j.namespace=p.slice(0).sort().join(".")):(p=[],j.namespace=""),j.type=n,j.guid||(j.guid=f.guid);var q=l[n],r=d.event.special[n]||{};if(!q){q=l[n]=[];if(!r.setup||r.setup.call(c,g,p,m)===!1)c.addEventListener?c.addEventListener(n,m,!1):c.attachEvent&&c.attachEvent("on"+n,m)}r.add&&(r.add.call(c,j),j.handler.guid||(j.handler.guid=f.guid)),q.push(j),d.event.global[n]=!0}c=null}},global:{},remove:function(a,c,e,f){if(a.nodeType!==3&&a.nodeType!==8){e===!1&&(e=v);var g,h,i,j,k=0,l,m,n,o,p,q,r,s=d.hasData(a)&&d._data(a),t=s&&s.events;if(!s||!t)return;c&&c.type&&(e=c.handler,c=c.type);if(!c||typeof c==="string"&&c.charAt(0)==="."){c=c||"";for(h in t)d.event.remove(a,h+c);return}c=c.split(" ");while(h=c[k++]){r=h,q=null,l=h.indexOf(".")<0,m=[],l||(m=h.split("."),h=m.shift(),n=new RegExp("(^|\\.)"+d.map(m.slice(0).sort(),u).join("\\.(?:.*\\.)?")+"(\\.|$)")),p=t[h];if(!p)continue;if(!e){for(j=0;j<p.length;j++){q=p[j];if(l||n.test(q.namespace))d.event.remove(a,r,q.handler,j),p.splice(j--,1)}continue}o=d.event.special[h]||{};for(j=f||0;j<p.length;j++){q=p[j];if(e.guid===q.guid){if(l||n.test(q.namespace))f==null&&p.splice(j--,1),o.remove&&o.remove.call(a,q);if(f!=null)break}}if(p.length===0||f!=null&&p.length===1)(!o.teardown||o.teardown.call(a,m)===!1)&&d.removeEvent(a,h,s.handle),g=null,delete t[h]}if(d.isEmptyObject(t)){var w=s.handle;w&&(w.elem=null),delete s.events,delete s.handle,d.isEmptyObject(s)&&d.removeData(a,b,!0)}}},trigger:function(a,c,e){var f=a.type||a,g=arguments[3];if(!g){a=typeof a==="object"?a[d.expando]?a:d.extend(d.Event(f),a):d.Event(f),f.indexOf("!")>=0&&(a.type=f=f.slice(0,-1),a.exclusive=!0),e||(a.stopPropagation(),d.event.global[f]&&d.each(d.cache,function(){var b=d.expando,e=this[b];e&&e.events&&e.events[f]&&d.event.trigger(a,c,e.handle.elem)}));if(!e||e.nodeType===3||e.nodeType===8)return b;a.result=b,a.target=e,c=d.makeArray(c),c.unshift(a)}a.currentTarget=e;var h=d._data(e,"handle");h&&h.apply(e,c);var i=e.parentNode||e.ownerDocument;try{e&&e.nodeName&&d.noData[e.nodeName.toLowerCase()]||e["on"+f]&&e["on"+f].apply(e,c)===!1&&(a.result=!1,a.preventDefault())}catch(j){}if(!a.isPropagationStopped()&&i)d.event.trigger(a,c,i,!0);else if(!a.isDefaultPrevented()){var k,l=a.target,m=f.replace(p,""),n=d.nodeName(l,"a")&&m==="click",o=d.event.special[m]||{};if((!o._default||o._default.call(e,a)===!1)&&!n&&!(l&&l.nodeName&&d.noData[l.nodeName.toLowerCase()])){try{l[m]&&(k=l["on"+m],k&&(l["on"+m]=null),d.event.triggered=!0,l[m]())}catch(q){}k&&(l["on"+m]=k),d.event.triggered=!1}}},handle:function(c){var e,f,g,h,i,j=[],k=d.makeArray(arguments);c=k[0]=d.event.fix(c||a.event),c.currentTarget=this,e=c.type.indexOf(".")<0&&!c.exclusive,e||(g=c.type.split("."),c.type=g.shift(),j=g.slice(0).sort(),h=new RegExp("(^|\\.)"+j.join("\\.(?:.*\\.)?")+"(\\.|$)")),c.namespace=c.namespace||j.join("."),i=d._data(this,"events"),f=(i||{})[c.type];if(i&&f){f=f.slice(0);for(var l=0,m=f.length;l<m;l++){var n=f[l];if(e||h.test(n.namespace)){c.handler=n.handler,c.data=n.data,c.handleObj=n;var o=n.handler.apply(this,k);o!==b&&(c.result=o,o===!1&&(c.preventDefault(),c.stopPropagation()));if(c.isImmediatePropagationStopped())break}}}return c.result},props:"altKey attrChange attrName bubbles button cancelable charCode clientX clientY ctrlKey currentTarget data detail eventPhase fromElement handler keyCode layerX layerY metaKey newValue offsetX offsetY pageX pageY prevValue relatedNode relatedTarget screenX screenY shiftKey srcElement target toElement view wheelDelta which".split(" "),fix:function(a){if(a[d.expando])return a;var e=a;a=d.Event(e);for(var f=this.props.length,g;f;)g=this.props[--f],a[g]=e[g];a.target||(a.target=a.srcElement||c),a.target.nodeType===3&&(a.target=a.target.parentNode),!a.relatedTarget&&a.fromElement&&(a.relatedTarget=a.fromElement===a.target?a.toElement:a.fromElement);if(a.pageX==null&&a.clientX!=null){var h=c.documentElement,i=c.body;a.pageX=a.clientX+(h&&h.scrollLeft||i&&i.scrollLeft||0)-(h&&h.clientLeft||i&&i.clientLeft||0),a.pageY=a.clientY+(h&&h.scrollTop||i&&i.scrollTop||0)-(h&&h.clientTop||i&&i.clientTop||0)}a.which==null&&(a.charCode!=null||a.keyCode!=null)&&(a.which=a.charCode!=null?a.charCode:a.keyCode),!a.metaKey&&a.ctrlKey&&(a.metaKey=a.ctrlKey),!a.which&&a.button!==b&&(a.which=a.button&1?1:a.button&2?3:a.button&4?2:0);return a},guid:1e8,proxy:d.proxy,special:{ready:{setup:d.bindReady,teardown:d.noop},live:{add:function(a){d.event.add(this,F(a.origType,a.selector),d.extend({},a,{handler:E,guid:a.handler.guid}))},remove:function(a){d.event.remove(this,F(a.origType,a.selector),a)}},beforeunload:{setup:function(a,b,c){d.isWindow(this)&&(this.onbeforeunload=c)},teardown:function(a,b){this.onbeforeunload===b&&(this.onbeforeunload=null)}}}},d.removeEvent=c.removeEventListener?function(a,b,c){a.removeEventListener&&a.removeEventListener(b,c,!1)}:function(a,b,c){a.detachEvent&&a.detachEvent("on"+b,c)},d.Event=function(a){if(!this.preventDefault)return new d.Event(a);a&&a.type?(this.originalEvent=a,this.type=a.type,this.isDefaultPrevented=a.defaultPrevented||a.returnValue===!1||a.getPreventDefault&&a.getPreventDefault()?w:v):this.type=a,this.timeStamp=d.now(),this[d.expando]=!0},d.Event.prototype={preventDefault:function(){this.isDefaultPrevented=w;var a=this.originalEvent;a&&(a.preventDefault?a.preventDefault():a.returnValue=!1)},stopPropagation:function(){this.isPropagationStopped=w;var a=this.originalEvent;a&&(a.stopPropagation&&a.stopPropagation(),a.cancelBubble=!0)},stopImmediatePropagation:function(){this.isImmediatePropagationStopped=w,this.stopPropagation()},isDefaultPrevented:v,isPropagationStopped:v,isImmediatePropagationStopped:v};var x=function(a){var b=a.relatedTarget;try{if(b!==c&&!b.parentNode)return;while(b&&b!==this)b=b.parentNode;b!==this&&(a.type=a.data,d.event.handle.apply(this,arguments))}catch(e){}},y=function(a){a.type=a.data,d.event.handle.apply(this,arguments)};d.each({mouseenter:"mouseover",mouseleave:"mouseout"},function(a,b){d.event.special[a]={setup:function(c){d.event.add(this,b,c&&c.selector?y:x,a)},teardown:function(a){d.event.remove(this,b,a&&a.selector?y:x)}}}),d.support.submitBubbles||(d.event.special.submit={setup:function(a,b){if(this.nodeName&&this.nodeName.toLowerCase()!=="form")d.event.add(this,"click.specialSubmit",function(a){var b=a.target,c=b.type;(c==="submit"||c==="image")&&d(b).closest("form").length&&C("submit",this,arguments)}),d.event.add(this,"keypress.specialSubmit",function(a){var b=a.target,c=b.type;(c==="text"||c==="password")&&d(b).closest("form").length&&a.keyCode===13&&C("submit",this,arguments)});else return!1},teardown:function(a){d.event.remove(this,".specialSubmit")}});if(!d.support.changeBubbles){var z,A=function(a){var b=a.type,c=a.value;b==="radio"||b==="checkbox"?c=a.checked:b==="select-multiple"?c=a.selectedIndex>-1?d.map(a.options,function(a){return a.selected}).join("-"):"":a.nodeName.toLowerCase()==="select"&&(c=a.selectedIndex);return c},B=function B(a){var c=a.target,e,f;if(q.test(c.nodeName)&&!c.readOnly){e=d._data(c,"_change_data"),f=A(c),(a.type!=="focusout"||c.type!=="radio")&&d._data(c,"_change_data",f);if(e===b||f===e)return;if(e!=null||f)a.type="change",a.liveFired=b,d.event.trigger(a,arguments[1],c)}};d.event.special.change={filters:{focusout:B,beforedeactivate:B,click:function(a){var b=a.target,c=b.type;(c==="radio"||c==="checkbox"||b.nodeName.toLowerCase()==="select")&&B.call(this,a)},keydown:function(a){var b=a.target,c=b.type;(a.keyCode===13&&b.nodeName.toLowerCase()!=="textarea"||a.keyCode===32&&(c==="checkbox"||c==="radio")||c==="select-multiple")&&B.call(this,a)},beforeactivate:function(a){var b=a.target;d._data(b,"_change_data",A(b))}},setup:function(a,b){if(this.type==="file")return!1;for(var c in z)d.event.add(this,c+".specialChange",z[c]);return q.test(this.nodeName)},teardown:function(a){d.event.remove(this,".specialChange");return q.test(this.nodeName)}},z=d.event.special.change.filters,z.focus=z.beforeactivate}c.addEventListener&&d.each({focus:"focusin",blur:"focusout"},function(a,b){function c(a){a=d.event.fix(a),a.type=b;return d.event.handle.call(this,a)}d.event.special[b]={setup:function(){this.addEventListener(a,c,!0)},teardown:function(){this.removeEventListener(a,c,!0)}}}),d.each(["bind","one"],function(a,c){d.fn[c]=function(a,e,f){if(typeof a==="object"){for(var g in a)this[c](g,e,a[g],f);return this}if(d.isFunction(e)||e===!1)f=e,e=b;var h=c==="one"?d.proxy(f,function(a){d(this).unbind(a,h);return f.apply(this,arguments)}):f;if(a==="unload"&&c!=="one")this.one(a,e,f);else for(var i=0,j=this.length;i<j;i++)d.event.add(this[i],a,h,e);return this}}),d.fn.extend({unbind:function(a,b){if(typeof a!=="object"||a.preventDefault)for(var e=0,f=this.length;e<f;e++)d.event.remove(this[e],a,b);else for(var c in a)this.unbind(c,a[c]);return this},delegate:function(a,b,c,d){return this.live(b,c,d,a)},undelegate:function(a,b,c){return arguments.length===0?this.unbind("live"):this.die(b,null,c,a)},trigger:function(a,b){return this.each(function(){d.event.trigger(a,b,this)})},triggerHandler:function(a,b){if(this[0]){var c=d.Event(a);c.preventDefault(),c.stopPropagation(),d.event.trigger(c,b,this[0]);return c.result}},toggle:function(a){var b=arguments,c=1;while(c<b.length)d.proxy(a,b[c++]);return this.click(d.proxy(a,function(e){var f=(d._data(this,"lastToggle"+a.guid)||0)%c;d._data(this,"lastToggle"+a.guid,f+1),e.preventDefault();return b[f].apply(this,arguments)||!1}))},hover:function(a,b){return this.mouseenter(a).mouseleave(b||a)}});var D={focus:"focusin",blur:"focusout",mouseenter:"mouseover",mouseleave:"mouseout"};d.each(["live","die"],function(a,c){d.fn[c]=function(a,e,f,g){var h,i=0,j,k,l,m=g||this.selector,n=g?this:d(this.context);if(typeof a==="object"&&!a.preventDefault){for(var o in a)n[c](o,e,a[o],m);return this}d.isFunction(e)&&(f=e,e=b),a=(a||"").split(" ");while((h=a[i++])!=null){j=p.exec(h),k="",j&&(k=j[0],h=h.replace(p,""));if(h==="hover"){a.push("mouseenter"+k,"mouseleave"+k);continue}l=h,h==="focus"||h==="blur"?(a.push(D[h]+k),h=h+k):h=(D[h]||h)+k;if(c==="live")for(var q=0,r=n.length;q<r;q++)d.event.add(n[q],"live."+F(h,m),{data:e,selector:m,handler:f,origType:h,origHandler:f,preType:l});else n.unbind("live."+F(h,m),f)}return this}}),d.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error".split(" "),function(a,b){d.fn[b]=function(a,c){c==null&&(c=a,a=null);return arguments.length>0?this.bind(b,a,c):this.trigger(b)},d.attrFn&&(d.attrFn[b]=!0)}),function(){function u(a,b,c,d,e,f){for(var g=0,h=d.length;g<h;g++){var i=d[g];if(i){var j=!1;i=i[a];while(i){if(i.sizcache===c){j=d[i.sizset];break}if(i.nodeType===1){f||(i.sizcache=c,i.sizset=g);if(typeof b!=="string"){if(i===b){j=!0;break}}else if(k.filter(b,[i]).length>0){j=i;break}}i=i[a]}d[g]=j}}}function t(a,b,c,d,e,f){for(var g=0,h=d.length;g<h;g++){var i=d[g];if(i){var j=!1;i=i[a];while(i){if(i.sizcache===c){j=d[i.sizset];break}i.nodeType===1&&!f&&(i.sizcache=c,i.sizset=g);if(i.nodeName.toLowerCase()===b){j=i;break}i=i[a]}d[g]=j}}}var a=/((?:\((?:\([^()]+\)|[^()]+)+\)|\[(?:\[[^\[\]]*\]|['"][^'"]*['"]|[^\[\]'"]+)+\]|\\.|[^ >+~,(\[\\]+)+|[>+~])(\s*,\s*)?((?:.|\r|\n)*)/g,e=0,f=Object.prototype.toString,g=!1,h=!0,i=/\\/g,j=/\W/;[0,0].sort(function(){h=!1;return 0});var k=function(b,d,e,g){e=e||[],d=d||c;var h=d;if(d.nodeType!==1&&d.nodeType!==9)return[];if(!b||typeof b!=="string")return e;var i,j,n,o,q,r,s,t,u=!0,w=k.isXML(d),x=[],y=b;do{a.exec(""),i=a.exec(y);if(i){y=i[3],x.push(i[1]);if(i[2]){o=i[3];break}}}while(i);if(x.length>1&&m.exec(b))if(x.length===2&&l.relative[x[0]])j=v(x[0]+x[1],d);else{j=l.relative[x[0]]?[d]:k(x.shift(),d);while(x.length)b=x.shift(),l.relative[b]&&(b+=x.shift()),j=v(b,j)}else{!g&&x.length>1&&d.nodeType===9&&!w&&l.match.ID.test(x[0])&&!l.match.ID.test(x[x.length-1])&&(q=k.find(x.shift(),d,w),d=q.expr?k.filter(q.expr,q.set)[0]:q.set[0]);if(d){q=g?{expr:x.pop(),set:p(g)}:k.find(x.pop(),x.length===1&&(x[0]==="~"||x[0]==="+")&&d.parentNode?d.parentNode:d,w),j=q.expr?k.filter(q.expr,q.set):q.set,x.length>0?n=p(j):u=!1;while(x.length)r=x.pop(),s=r,l.relative[r]?s=x.pop():r="",s==null&&(s=d),l.relative[r](n,s,w)}else n=x=[]}n||(n=j),n||k.error(r||b);if(f.call(n)==="[object Array]")if(u)if(d&&d.nodeType===1)for(t=0;n[t]!=null;t++)n[t]&&(n[t]===!0||n[t].nodeType===1&&k.contains(d,n[t]))&&e.push(j[t]);else for(t=0;n[t]!=null;t++)n[t]&&n[t].nodeType===1&&e.push(j[t]);else e.push.apply(e,n);else p(n,e);o&&(k(o,h,e,g),k.uniqueSort(e));return e};k.uniqueSort=function(a){if(r){g=h,a.sort(r);if(g)for(var b=1;b<a.length;b++)a[b]===a[b-1]&&a.splice(b--,1)}return a},k.matches=function(a,b){return k(a,null,null,b)},k.matchesSelector=function(a,b){return k(b,null,null,[a]).length>0},k.find=function(a,b,c){var d;if(!a)return[];for(var e=0,f=l.order.length;e<f;e++){var g,h=l.order[e];if(g=l.leftMatch[h].exec(a)){var j=g[1];g.splice(1,1);if(j.substr(j.length-1)!=="\\"){g[1]=(g[1]||"").replace(i,""),d=l.find[h](g,b,c);if(d!=null){a=a.replace(l.match[h],"");break}}}}d||(d=typeof b.getElementsByTagName!=="undefined"?b.getElementsByTagName("*"):[]);return{set:d,expr:a}},k.filter=function(a,c,d,e){var f,g,h=a,i=[],j=c,m=c&&c[0]&&k.isXML(c[0]);while(a&&c.length){for(var n in l.filter)if((f=l.leftMatch[n].exec(a))!=null&&f[2]){var o,p,q=l.filter[n],r=f[1];g=!1,f.splice(1,1);if(r.substr(r.length-1)==="\\")continue;j===i&&(i=[]);if(l.preFilter[n]){f=l.preFilter[n](f,j,d,i,e,m);if(f){if(f===!0)continue}else g=o=!0}if(f)for(var s=0;(p=j[s])!=null;s++)if(p){o=q(p,f,s,j);var t=e^!!o;d&&o!=null?t?g=!0:j[s]=!1:t&&(i.push(p),g=!0)}if(o!==b){d||(j=i),a=a.replace(l.match[n],"");if(!g)return[];break}}if(a===h)if(g==null)k.error(a);else break;h=a}return j},k.error=function(a){throw"Syntax error, unrecognized expression: "+a};var l=k.selectors={order:["ID","NAME","TAG"],match:{ID:/#((?:[\w\u00c0-\uFFFF\-]|\\.)+)/,CLASS:/\.((?:[\w\u00c0-\uFFFF\-]|\\.)+)/,NAME:/\[name=['"]*((?:[\w\u00c0-\uFFFF\-]|\\.)+)['"]*\]/,ATTR:/\[\s*((?:[\w\u00c0-\uFFFF\-]|\\.)+)\s*(?:(\S?=)\s*(?:(['"])(.*?)\3|(#?(?:[\w\u00c0-\uFFFF\-]|\\.)*)|)|)\s*\]/,TAG:/^((?:[\w\u00c0-\uFFFF\*\-]|\\.)+)/,CHILD:/:(only|nth|last|first)-child(?:\(\s*(even|odd|(?:[+\-]?\d+|(?:[+\-]?\d*)?n\s*(?:[+\-]\s*\d+)?))\s*\))?/,POS:/:(nth|eq|gt|lt|first|last|even|odd)(?:\((\d*)\))?(?=[^\-]|$)/,PSEUDO:/:((?:[\w\u00c0-\uFFFF\-]|\\.)+)(?:\((['"]?)((?:\([^\)]+\)|[^\(\)]*)+)\2\))?/},leftMatch:{},attrMap:{"class":"className","for":"htmlFor"},attrHandle:{href:function(a){return a.getAttribute("href")},type:function(a){return a.getAttribute("type")}},relative:{"+":function(a,b){var c=typeof b==="string",d=c&&!j.test(b),e=c&&!d;d&&(b=b.toLowerCase());for(var f=0,g=a.length,h;f<g;f++)if(h=a[f]){while((h=h.previousSibling)&&h.nodeType!==1){}a[f]=e||h&&h.nodeName.toLowerCase()===b?h||!1:h===b}e&&k.filter(b,a,!0)},">":function(a,b){var c,d=typeof b==="string",e=0,f=a.length;if(d&&!j.test(b)){b=b.toLowerCase();for(;e<f;e++){c=a[e];if(c){var g=c.parentNode;a[e]=g.nodeName.toLowerCase()===b?g:!1}}}else{for(;e<f;e++)c=a[e],c&&(a[e]=d?c.parentNode:c.parentNode===b);d&&k.filter(b,a,!0)}},"":function(a,b,c){var d,f=e++,g=u;typeof b==="string"&&!j.test(b)&&(b=b.toLowerCase(),d=b,g=t),g("parentNode",b,f,a,d,c)},"~":function(a,b,c){var d,f=e++,g=u;typeof b==="string"&&!j.test(b)&&(b=b.toLowerCase(),d=b,g=t),g("previousSibling",b,f,a,d,c)}},find:{ID:function(a,b,c){if(typeof b.getElementById!=="undefined"&&!c){var d=b.getElementById(a[1]);return d&&d.parentNode?[d]:[]}},NAME:function(a,b){if(typeof b.getElementsByName!=="undefined"){var c=[],d=b.getElementsByName(a[1]);for(var e=0,f=d.length;e<f;e++)d[e].getAttribute("name")===a[1]&&c.push(d[e]);return c.length===0?null:c}},TAG:function(a,b){if(typeof b.getElementsByTagName!=="undefined")return b.getElementsByTagName(a[1])}},preFilter:{CLASS:function(a,b,c,d,e,f){a=" "+a[1].replace(i,"")+" ";if(f)return a;for(var g=0,h;(h=b[g])!=null;g++)h&&(e^(h.className&&(" "+h.className+" ").replace(/[\t\n\r]/g," ").indexOf(a)>=0)?c||d.push(h):c&&(b[g]=!1));return!1},ID:function(a){return a[1].replace(i,"")},TAG:function(a,b){return a[1].replace(i,"").toLowerCase()},CHILD:function(a){if(a[1]==="nth"){a[2]||k.error(a[0]),a[2]=a[2].replace(/^\+|\s*/g,"");var b=/(-?)(\d*)(?:n([+\-]?\d*))?/.exec(a[2]==="even"&&"2n"||a[2]==="odd"&&"2n+1"||!/\D/.test(a[2])&&"0n+"+a[2]||a[2]);a[2]=b[1]+(b[2]||1)-0,a[3]=b[3]-0}else a[2]&&k.error(a[0]);a[0]=e++;return a},ATTR:function(a,b,c,d,e,f){var g=a[1]=a[1].replace(i,"");!f&&l.attrMap[g]&&(a[1]=l.attrMap[g]),a[4]=(a[4]||a[5]||"").replace(i,""),a[2]==="~="&&(a[4]=" "+a[4]+" ");return a},PSEUDO:function(b,c,d,e,f){if(b[1]==="not")if((a.exec(b[3])||"").length>1||/^\w/.test(b[3]))b[3]=k(b[3],null,null,c);else{var g=k.filter(b[3],c,d,!0^f);d||e.push.apply(e,g);return!1}else if(l.match.POS.test(b[0])||l.match.CHILD.test(b[0]))return!0;return b},POS:function(a){a.unshift(!0);return a}},filters:{enabled:function(a){return a.disabled===!1&&a.type!=="hidden"},disabled:function(a){return a.disabled===!0},checked:function(a){return a.checked===!0},selected:function(a){a.parentNode&&a.parentNode.selectedIndex;return a.selected===!0},parent:function(a){return!!a.firstChild},empty:function(a){return!a.firstChild},has:function(a,b,c){return!!k(c[3],a).length},header:function(a){return/h\d/i.test(a.nodeName)},text:function(a){return"text"===a.getAttribute("type")},radio:function(a){return"radio"===a.type},checkbox:function(a){return"checkbox"===a.type},file:function(a){return"file"===a.type},password:function(a){return"password"===a.type},submit:function(a){return"submit"===a.type},image:function(a){return"image"===a.type},reset:function(a){return"reset"===a.type},button:function(a){return"button"===a.type||a.nodeName.toLowerCase()==="button"},input:function(a){return/input|select|textarea|button/i.test(a.nodeName)}},setFilters:{first:function(a,b){return b===0},last:function(a,b,c,d){return b===d.length-1},even:function(a,b){return b%2===0},odd:function(a,b){return b%2===1},lt:function(a,b,c){return b<c[3]-0},gt:function(a,b,c){return b>c[3]-0},nth:function(a,b,c){return c[3]-0===b},eq:function(a,b,c){return c[3]-0===b}},filter:{PSEUDO:function(a,b,c,d){var e=b[1],f=l.filters[e];if(f)return f(a,c,b,d);if(e==="contains")return(a.textContent||a.innerText||k.getText([a])||"").indexOf(b[3])>=0;if(e==="not"){var g=b[3];for(var h=0,i=g.length;h<i;h++)if(g[h]===a)return!1;return!0}k.error(e)},CHILD:function(a,b){var c=b[1],d=a;switch(c){case"only":case"first":while(d=d.previousSibling)if(d.nodeType===1)return!1;if(c==="first")return!0;d=a;case"last":while(d=d.nextSibling)if(d.nodeType===1)return!1;return!0;case"nth":var e=b[2],f=b[3];if(e===1&&f===0)return!0;var g=b[0],h=a.parentNode;if(h&&(h.sizcache!==g||!a.nodeIndex)){var i=0;for(d=h.firstChild;d;d=d.nextSibling)d.nodeType===1&&(d.nodeIndex=++i);h.sizcache=g}var j=a.nodeIndex-f;return e===0?j===0:j%e===0&&j/e>=0}},ID:function(a,b){return a.nodeType===1&&a.getAttribute("id")===b},TAG:function(a,b){return b==="*"&&a.nodeType===1||a.nodeName.toLowerCase()===b},CLASS:function(a,b){return(" "+(a.className||a.getAttribute("class"))+" ").indexOf(b)>-1},ATTR:function(a,b){var c=b[1],d=l.attrHandle[c]?l.attrHandle[c](a):a[c]!=null?a[c]:a.getAttribute(c),e=d+"",f=b[2],g=b[4];return d==null?f==="!=":f==="="?e===g:f==="*="?e.indexOf(g)>=0:f==="~="?(" "+e+" ").indexOf(g)>=0:g?f==="!="?e!==g:f==="^="?e.indexOf(g)===0:f==="$="?e.substr(e.length-g.length)===g:f==="|="?e===g||e.substr(0,g.length+1)===g+"-":!1:e&&d!==!1},POS:function(a,b,c,d){var e=b[2],f=l.setFilters[e];if(f)return f(a,c,b,d)}}},m=l.match.POS,n=function(a,b){return"\\"+(b-0+1)};for(var o in l.match)l.match[o]=new RegExp(l.match[o].source+/(?![^\[]*\])(?![^\(]*\))/.source),l.leftMatch[o]=new RegExp(/(^(?:.|\r|\n)*?)/.source+l.match[o].source.replace(/\\(\d+)/g,n));var p=function(a,b){a=Array.prototype.slice.call(a,0);if(b){b.push.apply(b,a);return b}return a};try{Array.prototype.slice.call(c.documentElement.childNodes,0)[0].nodeType}catch(q){p=function(a,b){var c=0,d=b||[];if(f.call(a)==="[object Array]")Array.prototype.push.apply(d,a);else if(typeof a.length==="number")for(var e=a.length;c<e;c++)d.push(a[c]);else for(;a[c];c++)d.push(a[c]);return d}}var r,s;c.documentElement.compareDocumentPosition?r=function(a,b){if(a===b){g=!0;return 0}if(!a.compareDocumentPosition||!b.compareDocumentPosition)return a.compareDocumentPosition?-1:1;return a.compareDocumentPosition(b)&4?-1:1}:(r=function(a,b){var c,d,e=[],f=[],h=a.parentNode,i=b.parentNode,j=h;if(a===b){g=!0;return 0}if(h===i)return s(a,b);if(!h)return-1;if(!i)return 1;while(j)e.unshift(j),j=j.parentNode;j=i;while(j)f.unshift(j),j=j.parentNode;c=e.length,d=f.length;for(var k=0;k<c&&k<d;k++)if(e[k]!==f[k])return s(e[k],f[k]);return k===c?s(a,f[k],-1):s(e[k],b,1)},s=function(a,b,c){if(a===b)return c;var d=a.nextSibling;while(d){if(d===b)return-1;d=d.nextSibling}return 1}),k.getText=function(a){var b="",c;for(var d=0;a[d];d++)c=a[d],c.nodeType===3||c.nodeType===4?b+=c.nodeValue:c.nodeType!==8&&(b+=k.getText(c.childNodes));return b},function(){var a=c.createElement("div"),d="script"+(new Date).getTime(),e=c.documentElement;a.innerHTML="<a name='"+d+"'/>",e.insertBefore(a,e.firstChild),c.getElementById(d)&&(l.find.ID=function(a,c,d){if(typeof c.getElementById!=="undefined"&&!d){var e=c.getElementById(a[1]);return e?e.id===a[1]||typeof e.getAttributeNode!=="undefined"&&e.getAttributeNode("id").nodeValue===a[1]?[e]:b:[]}},l.filter.ID=function(a,b){var c=typeof a.getAttributeNode!=="undefined"&&a.getAttributeNode("id");return a.nodeType===1&&c&&c.nodeValue===b}),e.removeChild(a),e=a=null}(),function(){var a=c.createElement("div");a.appendChild(c.createComment("")),a.getElementsByTagName("*").length>0&&(l.find.TAG=function(a,b){var c=b.getElementsByTagName(a[1]);if(a[1]==="*"){var d=[];for(var e=0;c[e];e++)c[e].nodeType===1&&d.push(c[e]);c=d}return c}),a.innerHTML="<a href='#'></a>",a.firstChild&&typeof a.firstChild.getAttribute!=="undefined"&&a.firstChild.getAttribute("href")!=="#"&&(l.attrHandle.href=function(a){return a.getAttribute("href",2)}),a=null}(),c.querySelectorAll&&function(){var a=k,b=c.createElement("div"),d="__sizzle__";b.innerHTML="<p class='TEST'></p>";if(!b.querySelectorAll||b.querySelectorAll(".TEST").length!==0){k=function(b,e,f,g){e=e||c;if(!g&&!k.isXML(e)){var h=/^(\w+$)|^\.([\w\-]+$)|^#([\w\-]+$)/.exec(b);if(h&&(e.nodeType===1||e.nodeType===9)){if(h[1])return p(e.getElementsByTagName(b),f);if(h[2]&&l.find.CLASS&&e.getElementsByClassName)return p(e.getElementsByClassName(h[2]),f)}if(e.nodeType===9){if(b==="body"&&e.body)return p([e.body],f);if(h&&h[3]){var i=e.getElementById(h[3]);if(!i||!i.parentNode)return p([],f);if(i.id===h[3])return p([i],f)}try{return p(e.querySelectorAll(b),f)}catch(j){}}else if(e.nodeType===1&&e.nodeName.toLowerCase()!=="object"){var m=e,n=e.getAttribute("id"),o=n||d,q=e.parentNode,r=/^\s*[+~]/.test(b);n?o=o.replace(/'/g,"\\$&"):e.setAttribute("id",o),r&&q&&(e=e.parentNode);try{if(!r||q)return p(e.querySelectorAll("[id='"+o+"'] "+b),f)}catch(s){}finally{n||m.removeAttribute("id")}}}return a(b,e,f,g)};for(var e in a)k[e]=a[e];b=null}}(),function(){var a=c.documentElement,b=a.matchesSelector||a.mozMatchesSelector||a.webkitMatchesSelector||a.msMatchesSelector,d=!1;try{b.call(c.documentElement,"[test!='']:sizzle")}catch(e){d=!0}b&&(k.matchesSelector=function(a,c){c=c.replace(/\=\s*([^'"\]]*)\s*\]/g,"='$1']");if(!k.isXML(a))try{if(d||!l.match.PSEUDO.test(c)&&!/!=/.test(c))return b.call(a,c)}catch(e){}return k(c,null,null,[a]).length>0})}(),function(){var a=c.createElement("div");a.innerHTML="<div class='test e'></div><div class='test'></div>";if(a.getElementsByClassName&&a.getElementsByClassName("e").length!==0){a.lastChild.className="e";if(a.getElementsByClassName("e").length===1)return;l.order.splice(1,0,"CLASS"),l.find.CLASS=function(a,b,c){if(typeof b.getElementsByClassName!=="undefined"&&!c)return b.getElementsByClassName(a[1])},a=null}}(),c.documentElement.contains?k.contains=function(a,b){return a!==b&&(a.contains?a.contains(b):!0)}:c.documentElement.compareDocumentPosition?k.contains=function(a,b){return!!(a.compareDocumentPosition(b)&16)}:k.contains=function(){return!1},k.isXML=function(a){var b=(a?a.ownerDocument||a:0).documentElement;return b?b.nodeName!=="HTML":!1};var v=function(a,b){var c,d=[],e="",f=b.nodeType?[b]:b;while(c=l.match.PSEUDO.exec(a))e+=c[0],a=a.replace(l.match.PSEUDO,"");a=l.relative[a]?a+"*":a;for(var g=0,h=f.length;g<h;g++)k(a,f[g],d);return k.filter(e,d)};d.find=k,d.expr=k.selectors,d.expr[":"]=d.expr.filters,d.unique=k.uniqueSort,d.text=k.getText,d.isXMLDoc=k.isXML,d.contains=k.contains}();var G=/Until$/,H=/^(?:parents|prevUntil|prevAll)/,I=/,/,J=/^.[^:#\[\.,]*$/,K=Array.prototype.slice,L=d.expr.match.POS,M={children:!0,contents:!0,next:!0,prev:!0};d.fn.extend({find:function(a){var b=this.pushStack("","find",a),c=0;for(var e=0,f=this.length;e<f;e++){c=b.length,d.find(a,this[e],b);if(e>0)for(var g=c;g<b.length;g++)for(var h=0;h<c;h++)if(b[h]===b[g]){b.splice(g--,1);break}}return b},has:function(a){var b=d(a);return this.filter(function(){for(var a=0,c=b.length;a<c;a++)if(d.contains(this,b[a]))return!0})},not:function(a){return this.pushStack(O(this,a,!1),"not",a)},filter:function(a){return this.pushStack(O(this,a,!0),"filter",a)},is:function(a){return!!a&&d.filter(a,this).length>0},closest:function(a,b){var c=[],e,f,g=this[0];if(d.isArray(a)){var h,i,j={},k=1;if(g&&a.length){for(e=0,f=a.length;e<f;e++)i=a[e],j[i]||(j[i]=d.expr.match.POS.test(i)?d(i,b||this.context):i);while(g&&g.ownerDocument&&g!==b){for(i in j)h=j[i],(h.jquery?h.index(g)>-1:d(g).is(h))&&c.push({selector:i,elem:g,level:k});g=g.parentNode,k++}}return c}var l=L.test(a)?d(a,b||this.context):null;for(e=0,f=this.length;e<f;e++){g=this[e];while(g){if(l?l.index(g)>-1:d.find.matchesSelector(g,a)){c.push(g);break}g=g.parentNode;if(!g||!g.ownerDocument||g===b)break}}c=c.length>1?d.unique(c):c;return this.pushStack(c,"closest",a)},index:function(a){if(!a||typeof a==="string")return d.inArray(this[0],a?d(a):this.parent().children());return d.inArray(a.jquery?a[0]:a,this)},add:function(a,b){var c=typeof a==="string"?d(a,b):d.makeArray(a),e=d.merge(this.get(),c);return this.pushStack(N(c[0])||N(e[0])?e:d.unique(e))},andSelf:function(){return this.add(this.prevObject)}}),d.each({parent:function(a){var b=a.parentNode;return b&&b.nodeType!==11?b:null},parents:function(a){return d.dir(a,"parentNode")},parentsUntil:function(a,b,c){return d.dir(a,"parentNode",c)},next:function(a){return d.nth(a,2,"nextSibling")},prev:function(a){return d.nth(a,2,"previousSibling")},nextAll:function(a){return d.dir(a,"nextSibling")},prevAll:function(a){return d.dir(a,"previousSibling")},nextUntil:function(a,b,c){return d.dir(a,"nextSibling",c)},prevUntil:function(a,b,c){return d.dir(a,"previousSibling",c)},siblings:function(a){return d.sibling(a.parentNode.firstChild,a)},children:function(a){return d.sibling(a.firstChild)},contents:function(a){return d.nodeName(a,"iframe")?a.contentDocument||a.contentWindow.document:d.makeArray(a.childNodes)}},function(a,b){d.fn[a]=function(c,e){var f=d.map(this,b,c),g=K.call(arguments);G.test(a)||(e=c),e&&typeof e==="string"&&(f=d.filter(e,f)),f=this.length>1&&!M[a]?d.unique(f):f,(this.length>1||I.test(e))&&H.test(a)&&(f=f.reverse());return this.pushStack(f,a,g.join(","))}}),d.extend({filter:function(a,b,c){c&&(a=":not("+a+")");return b.length===1?d.find.matchesSelector(b[0],a)?[b[0]]:[]:d.find.matches(a,b)},dir:function(a,c,e){var f=[],g=a[c];while(g&&g.nodeType!==9&&(e===b||g.nodeType!==1||!d(g).is(e)))g.nodeType===1&&f.push(g),g=g[c];return f},nth:function(a,b,c,d){b=b||1;var e=0;for(;a;a=a[c])if(a.nodeType===1&&++e===b)break;return a},sibling:function(a,b){var c=[];for(;a;a=a.nextSibling)a.nodeType===1&&a!==b&&c.push(a);return c}});var P=/ jQuery\d+="(?:\d+|null)"/g,Q=/^\s+/,R=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/ig,S=/<([\w:]+)/,T=/<tbody/i,U=/<|&#?\w+;/,V=/<(?:script|object|embed|option|style)/i,W=/checked\s*(?:[^=]|=\s*.checked.)/i,X={option:[1,"<select multiple='multiple'>","</select>"],legend:[1,"<fieldset>","</fieldset>"],thead:[1,"<table>","</table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],col:[2,"<table><tbody></tbody><colgroup>","</colgroup></table>"],area:[1,"<map>","</map>"],_default:[0,"",""]};X.optgroup=X.option,X.tbody=X.tfoot=X.colgroup=X.caption=X.thead,X.th=X.td,d.support.htmlSerialize||(X._default=[1,"div<div>","</div>"]),d.fn.extend({text:function(a){if(d.isFunction(a))return this.each(function(b){var c=d(this);c.text(a.call(this,b,c.text()))});if(typeof a!=="object"&&a!==b)return this.empty().append((this[0]&&this[0].ownerDocument||c).createTextNode(a));return d.text(this)},wrapAll:function(a){if(d.isFunction(a))return this.each(function(b){d(this).wrapAll(a.call(this,b))});if(this[0]){var b=d(a,this[0].ownerDocument).eq(0).clone(!0);this[0].parentNode&&b.insertBefore(this[0]),b.map(function(){var a=this;while(a.firstChild&&a.firstChild.nodeType===1)a=a.firstChild;return a}).append(this)}return this},wrapInner:function(a){if(d.isFunction(a))return this.each(function(b){d(this).wrapInner(a.call(this,b))});return this.each(function(){var b=d(this),c=b.contents();c.length?c.wrapAll(a):b.append(a)})},wrap:function(a){return this.each(function(){d(this).wrapAll(a)})},unwrap:function(){return this.parent().each(function(){d.nodeName(this,"body")||d(this).replaceWith(this.childNodes)}).end()},append:function(){return this.domManip(arguments,!0,function(a){this.nodeType===1&&this.appendChild(a)})},prepend:function(){return this.domManip(arguments,!0,function(a){this.nodeType===1&&this.insertBefore(a,this.firstChild)})},before:function(){if(this[0]&&this[0].parentNode)return this.domManip(arguments,!1,function(a){this.parentNode.insertBefore(a,this)});if(arguments.length){var a=d(arguments[0]);a.push.apply(a,this.toArray());return this.pushStack(a,"before",arguments)}},after:function(){if(this[0]&&this[0].parentNode)return this.domManip(arguments,!1,function(a){this.parentNode.insertBefore(a,this.nextSibling)});if(arguments.length){var a=this.pushStack(this,"after",arguments);a.push.apply(a,d(arguments[0]).toArray());return a}},remove:function(a,b){for(var c=0,e;(e=this[c])!=null;c++)if(!a||d.filter(a,[e]).length)!b&&e.nodeType===1&&(d.cleanData(e.getElementsByTagName("*")),d.cleanData([e])),e.parentNode&&e.parentNode.removeChild(e);return this},empty:function(){for(var a=0,b;(b=this[a])!=null;a++){b.nodeType===1&&d.cleanData(b.getElementsByTagName("*"));while(b.firstChild)b.removeChild(b.firstChild)}return this},clone:function(a,b){a=a==null?!1:a,b=b==null?a:b;return this.map(function(){return d.clone(this,a,b)})},html:function(a){if(a===b)return this[0]&&this[0].nodeType===1?this[0].innerHTML.replace(P,""):null;if(typeof a!=="string"||V.test(a)||!d.support.leadingWhitespace&&Q.test(a)||X[(S.exec(a)||["",""])[1].toLowerCase()])d.isFunction(a)?this.each(function(b){var c=d(this);c.html(a.call(this,b,c.html()))}):this.empty().append(a);else{a=a.replace(R,"<$1></$2>");try{for(var c=0,e=this.length;c<e;c++)this[c].nodeType===1&&(d.cleanData(this[c].getElementsByTagName("*")),this[c].innerHTML=a)}catch(f){this.empty().append(a)}}return this},replaceWith:function(a){if(this[0]&&this[0].parentNode){if(d.isFunction(a))return this.each(function(b){var c=d(this),e=c.html();c.replaceWith(a.call(this,b,e))});typeof a!=="string"&&(a=d(a).detach());return this.each(function(){var b=this.nextSibling,c=this.parentNode;d(this).remove(),b?d(b).before(a):d(c).append(a)})}return this.pushStack(d(d.isFunction(a)?a():a),"replaceWith",a)},detach:function(a){return this.remove(a,!0)},domManip:function(a,c,e){var f,g,h,i,j=a[0],k=[];if(!d.support.checkClone&&arguments.length===3&&typeof j==="string"&&W.test(j))return this.each(function(){d(this).domManip(a,c,e,!0)});if(d.isFunction(j))return this.each(function(f){var g=d(this);a[0]=j.call(this,f,c?g.html():b),g.domManip(a,c,e)});if(this[0]){i=j&&j.parentNode,d.support.parentNode&&i&&i.nodeType===11&&i.childNodes.length===this.length?f={fragment:i}:f=d.buildFragment(a,this,k),h=f.fragment,h.childNodes.length===1?g=h=h.firstChild:g=h.firstChild;if(g){c=c&&d.nodeName(g,"tr");for(var l=0,m=this.length,n=m-1;l<m;l++)e.call(c?Y(this[l],g):this[l],f.cacheable||m>1&&l<n?d.clone(h,!0,!0):h)}k.length&&d.each(k,ba)}return this}}),d.buildFragment=function(a,b,e){var f,g,h,i=b&&b[0]?b[0].ownerDocument||b[0]:c;a.length===1&&typeof a[0]==="string"&&a[0].length<512&&i===c&&a[0].charAt(0)==="<"&&!V.test(a[0])&&(d.support.checkClone||!W.test(a[0]))&&(g=!0,h=d.fragments[a[0]],h&&(h!==1&&(f=h))),f||(f=i.createDocumentFragment(),d.clean(a,i,f,e)),g&&(d.fragments[a[0]]=h?f:1);return{fragment:f,cacheable:g}},d.fragments={},d.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(a,b){d.fn[a]=function(c){var e=[],f=d(c),g=this.length===1&&this[0].parentNode;if(g&&g.nodeType===11&&g.childNodes.length===1&&f.length===1){f[b](this[0]);return this}for(var h=0,i=f.length;h<i;h++){var j=(h>0?this.clone(!0):this).get();d(f[h])[b](j),e=e.concat(j)}return this.pushStack(e,a,f.selector)}}),d.extend({clone:function(a,b,c){var e=a.cloneNode(!0),f,g,h;if((!d.support.noCloneEvent||!d.support.noCloneChecked)&&(a.nodeType===1||a.nodeType===11)&&!d.isXMLDoc(a)){$(a,e),f=_(a),g=_(e);for(h=0;f[h];++h)$(f[h],g[h])}if(b){Z(a,e);if(c){f=_(a),g=_(e);for(h=0;f[h];++h)Z(f[h],g[h])}}return e},clean:function(a,b,e,f){b=b||c,typeof b.createElement==="undefined"&&(b=b.ownerDocument||b[0]&&b[0].ownerDocument||c);var g=[];for(var h=0,i;(i=a[h])!=null;h++){typeof i==="number"&&(i+="");if(!i)continue;if(typeof i!=="string"||U.test(i)){if(typeof i==="string"){i=i.replace(R,"<$1></$2>");var j=(S.exec(i)||["",""])[1].toLowerCase(),k=X[j]||X._default,l=k[0],m=b.createElement("div");m.innerHTML=k[1]+i+k[2];while(l--)m=m.lastChild;if(!d.support.tbody){var n=T.test(i),o=j==="table"&&!n?m.firstChild&&m.firstChild.childNodes:k[1]==="<table>"&&!n?m.childNodes:[];for(var p=o.length-1;p>=0;--p)d.nodeName(o[p],"tbody")&&!o[p].childNodes.length&&o[p].parentNode.removeChild(o[p])}!d.support.leadingWhitespace&&Q.test(i)&&m.insertBefore(b.createTextNode(Q.exec(i)[0]),m.firstChild),i=m.childNodes}}else i=b.createTextNode(i);i.nodeType?g.push(i):g=d.merge(g,i)}if(e)for(h=0;g[h];h++)!f||!d.nodeName(g[h],"script")||g[h].type&&g[h].type.toLowerCase()!=="text/javascript"?(g[h].nodeType===1&&g.splice.apply(g,[h+1,0].concat(d.makeArray(g[h].getElementsByTagName("script")))),e.appendChild(g[h])):f.push(g[h].parentNode?g[h].parentNode.removeChild(g[h]):g[h]);return g},cleanData:function(a){var b,c,e=d.cache,f=d.expando,g=d.event.special,h=d.support.deleteExpando;for(var i=0,j;(j=a[i])!=null;i++){if(j.nodeName&&d.noData[j.nodeName.toLowerCase()])continue;c=j[d.expando];if(c){b=e[c]&&e[c][f];if(b&&b.events){for(var k in b.events)g[k]?d.event.remove(j,k):d.removeEvent(j,k,b.handle);b.handle&&(b.handle.elem=null)}h?delete j[d.expando]:j.removeAttribute&&j.removeAttribute(d.expando),delete e[c]}}}});var bb=/alpha\([^)]*\)/i,bc=/opacity=([^)]*)/,bd=/-([a-z])/ig,be=/([A-Z])/g,bf=/^-?\d+(?:px)?$/i,bg=/^-?\d/,bh={position:"absolute",visibility:"hidden",display:"block"},bi=["Left","Right"],bj=["Top","Bottom"],bk,bl,bm,bn=function(a,b){return b.toUpperCase()};d.fn.css=function(a,c){if(arguments.length===2&&c===b)return this;return d.access(this,a,c,!0,function(a,c,e){return e!==b?d.style(a,c,e):d.css(a,c)})},d.extend({cssHooks:{opacity:{get:function(a,b){if(b){var c=bk(a,"opacity","opacity");return c===""?"1":c}return a.style.opacity}}},cssNumber:{zIndex:!0,fontWeight:!0,opacity:!0,zoom:!0,lineHeight:!0},cssProps:{"float":d.support.cssFloat?"cssFloat":"styleFloat"},style:function(a,c,e,f){if(a&&a.nodeType!==3&&a.nodeType!==8&&a.style){var g,h=d.camelCase(c),i=a.style,j=d.cssHooks[h];c=d.cssProps[h]||h;if(e===b){if(j&&"get"in j&&(g=j.get(a,!1,f))!==b)return g;return i[c]}if(typeof e==="number"&&isNaN(e)||e==null)return;typeof e==="number"&&!d.cssNumber[h]&&(e+="px");if(!j||!("set"in j)||(e=j.set(a,e))!==b)try{i[c]=e}catch(k){}}},css:function(a,c,e){var f,g=d.camelCase(c),h=d.cssHooks[g];c=d.cssProps[g]||g;if(h&&"get"in h&&(f=h.get(a,!0,e))!==b)return f;if(bk)return bk(a,c,g)},swap:function(a,b,c){var d={};for(var e in b)d[e]=a.style[e],a.style[e]=b[e];c.call(a);for(e in b)a.style[e]=d[e]},camelCase:function(a){return a.replace(bd,bn)}}),d.curCSS=d.css,d.each(["height","width"],function(a,b){d.cssHooks[b]={get:function(a,c,e){var f;if(c){a.offsetWidth!==0?f=bo(a,b,e):d.swap(a,bh,function(){f=bo(a,b,e)});if(f<=0){f=bk(a,b,b),f==="0px"&&bm&&(f=bm(a,b,b));if(f!=null)return f===""||f==="auto"?"0px":f}if(f<0||f==null){f=a.style[b];return f===""||f==="auto"?"0px":f}return typeof f==="string"?f:f+"px"}},set:function(a,b){if(!bf.test(b))return b;b=parseFloat(b);if(b>=0)return b+"px"}}}),d.support.opacity||(d.cssHooks.opacity={get:function(a,b){return bc.test((b&&a.currentStyle?a.currentStyle.filter:a.style.filter)||"")?parseFloat(RegExp.$1)/100+"":b?"1":""},set:function(a,b){var c=a.style;c.zoom=1;var e=d.isNaN(b)?"":"alpha(opacity="+b*100+")",f=c.filter||"";c.filter=bb.test(f)?f.replace(bb,e):c.filter+" "+e}}),c.defaultView&&c.defaultView.getComputedStyle&&(bl=function(a,c,e){var f,g,h;e=e.replace(be,"-$1").toLowerCase();if(!(g=a.ownerDocument.defaultView))return b;if(h=g.getComputedStyle(a,null))f=h.getPropertyValue(e),f===""&&!d.contains(a.ownerDocument.documentElement,a)&&(f=d.style(a,e));return f}),c.documentElement.currentStyle&&(bm=function(a,b){var c,d=a.currentStyle&&a.currentStyle[b],e=a.runtimeStyle&&a.runtimeStyle[b],f=a.style;!bf.test(d)&&bg.test(d)&&(c=f.left,e&&(a.runtimeStyle.left=a.currentStyle.left),f.left=b==="fontSize"?"1em":d||0,d=f.pixelLeft+"px",f.left=c,e&&(a.runtimeStyle.left=e));return d===""?"auto":d}),bk=bl||bm,d.expr&&d.expr.filters&&(d.expr.filters.hidden=function(a){var b=a.offsetWidth,c=a.offsetHeight;return b===0&&c===0||!d.support.reliableHiddenOffsets&&(a.style.display||d.css(a,"display"))==="none"},d.expr.filters.visible=function(a){return!d.expr.filters.hidden(a)});var bp=/%20/g,bq=/\[\]$/,br=/\r?\n/g,bs=/#.*$/,bt=/^(.*?):[ \t]*([^\r\n]*)\r?$/mg,bu=/^(?:color|date|datetime|email|hidden|month|number|password|range|search|tel|text|time|url|week)$/i,bv=/(?:^file|^widget|\-extension):$/,bw=/^(?:GET|HEAD)$/,bx=/^\/\//,by=/\?/,bz=/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,bA=/^(?:select|textarea)/i,bB=/\s+/,bC=/([?&])_=[^&]*/,bD=/(^|\-)([a-z])/g,bE=function(a,b,c){return b+c.toUpperCase()},bF=/^([\w\+\.\-]+:)\/\/([^\/?#:]*)(?::(\d+))?/,bG=d.fn.load,bH={},bI={},bJ,bK;try{bJ=c.location.href}catch(bL){bJ=c.createElement("a"),bJ.href="",bJ=bJ.href}bK=bF.exec(bJ.toLowerCase()),d.fn.extend({load:function(a,c,e){if(typeof a!=="string"&&bG)return bG.apply(this,arguments);if(!this.length)return this;var f=a.indexOf(" ");if(f>=0){var g=a.slice(f,a.length);a=a.slice(0,f)}var h="GET";c&&(d.isFunction(c)?(e=c,c=b):typeof c==="object"&&(c=d.param(c,d.ajaxSettings.traditional),h="POST"));var i=this;d.ajax({url:a,type:h,dataType:"html",data:c,complete:function(a,b,c){c=a.responseText,a.isResolved()&&(a.done(function(a){c=a}),i.html(g?d("<div>").append(c.replace(bz,"")).find(g):c)),e&&i.each(e,[c,b,a])}});return this},serialize:function(){return d.param(this.serializeArray())},serializeArray:function(){return this.map(function(){return this.elements?d.makeArray(this.elements):this}).filter(function(){return this.name&&!this.disabled&&(this.checked||bA.test(this.nodeName)||bu.test(this.type))}).map(function(a,b){var c=d(this).val();return c==null?null:d.isArray(c)?d.map(c,function(a,c){return{name:b.name,value:a.replace(br,"\r\n")}}):{name:b.name,value:c.replace(br,"\r\n")}}).get()}}),d.each("ajaxStart ajaxStop ajaxComplete ajaxError ajaxSuccess ajaxSend".split(" "),function(a,b){d.fn[b]=function(a){return this.bind(b,a)}}),d.each(["get","post"],function(a,c){d[c]=function(a,e,f,g){d.isFunction(e)&&(g=g||f,f=e,e=b);return d.ajax({type:c,url:a,data:e,success:f,dataType:g})}}),d.extend({getScript:function(a,c){return d.get(a,b,c,"script")},getJSON:function(a,b,c){return d.get(a,b,c,"json")},ajaxSetup:function(a,b){b?d.extend(!0,a,d.ajaxSettings,b):(b=a,a=d.extend(!0,d.ajaxSettings,b));for(var c in {context:1,url:1})c in b?a[c]=b[c]:c in d.ajaxSettings&&(a[c]=d.ajaxSettings[c]);return a},ajaxSettings:{url:bJ,isLocal:bv.test(bK[1]),global:!0,type:"GET",contentType:"application/x-www-form-urlencoded",processData:!0,async:!0,accepts:{xml:"application/xml, text/xml",html:"text/html",text:"text/plain",json:"application/json, text/javascript","*":"*/*"},contents:{xml:/xml/,html:/html/,json:/json/},responseFields:{xml:"responseXML",text:"responseText"},converters:{"* text":a.String,"text html":!0,"text json":d.parseJSON,"text xml":d.parseXML}},ajaxPrefilter:bM(bH),ajaxTransport:bM(bI),ajax:function(a,c){function v(a,c,l,n){if(r!==2){r=2,p&&clearTimeout(p),o=b,m=n||"",u.readyState=a?4:0;var q,t,v,w=l?bP(e,u,l):b,x,y;if(a>=200&&a<300||a===304){if(e.ifModified){if(x=u.getResponseHeader("Last-Modified"))d.lastModified[k]=x;if(y=u.getResponseHeader("Etag"))d.etag[k]=y}if(a===304)c="notmodified",q=!0;else try{t=bQ(e,w),c="success",q=!0}catch(z){c="parsererror",v=z}}else{v=c;if(!c||a)c="error",a<0&&(a=0)}u.status=a,u.statusText=c,q?h.resolveWith(f,[t,c,u]):h.rejectWith(f,[u,c,v]),u.statusCode(j),j=b,s&&g.trigger("ajax"+(q?"Success":"Error"),[u,e,q?t:v]),i.resolveWith(f,[u,c]),s&&(g.trigger("ajaxComplete",[u,e]),--d.active||d.event.trigger("ajaxStop"))}}typeof a==="object"&&(c=a,a=b),c=c||{};var e=d.ajaxSetup({},c),f=e.context||e,g=f!==e&&(f.nodeType||f instanceof d)?d(f):d.event,h=d.Deferred(),i=d._Deferred(),j=e.statusCode||{},k,l={},m,n,o,p,q,r=0,s,t,u={readyState:0,setRequestHeader:function(a,b){r||(l[a.toLowerCase().replace(bD,bE)]=b);return this},getAllResponseHeaders:function(){return r===2?m:null},getResponseHeader:function(a){var c;if(r===2){if(!n){n={};while(c=bt.exec(m))n[c[1].toLowerCase()]=c[2]}c=n[a.toLowerCase()]}return c===b?null:c},overrideMimeType:function(a){r||(e.mimeType=a);return this},abort:function(a){a=a||"abort",o&&o.abort(a),v(0,a);return this}};h.promise(u),u.success=u.done,u.error=u.fail,u.complete=i.done,u.statusCode=function(a){if(a){var b;if(r<2)for(b in a)j[b]=[j[b],a[b]];else b=a[u.status],u.then(b,b)}return this},e.url=((a||e.url)+"").replace(bs,"").replace(bx,bK[1]+"//"),e.dataTypes=d.trim(e.dataType||"*").toLowerCase().split(bB),e.crossDomain||(q=bF.exec(e.url.toLowerCase()),e.crossDomain=q&&(q[1]!=bK[1]||q[2]!=bK[2]||(q[3]||(q[1]==="http:"?80:443))!=(bK[3]||(bK[1]==="http:"?80:443)))),e.data&&e.processData&&typeof e.data!=="string"&&(e.data=d.param(e.data,e.traditional)),bN(bH,e,c,u);if(r===2)return!1;s=e.global,e.type=e.type.toUpperCase(),e.hasContent=!bw.test(e.type),s&&d.active++===0&&d.event.trigger("ajaxStart");if(!e.hasContent){e.data&&(e.url+=(by.test(e.url)?"&":"?")+e.data),k=e.url;if(e.cache===!1){var w=d.now(),x=e.url.replace(bC,"$1_="+w);e.url=x+(x===e.url?(by.test(e.url)?"&":"?")+"_="+w:"")}}if(e.data&&e.hasContent&&e.contentType!==!1||c.contentType)l["Content-Type"]=e.contentType;e.ifModified&&(k=k||e.url,d.lastModified[k]&&(l["If-Modified-Since"]=d.lastModified[k]),d.etag[k]&&(l["If-None-Match"]=d.etag[k])),l.Accept=e.dataTypes[0]&&e.accepts[e.dataTypes[0]]?e.accepts[e.dataTypes[0]]+(e.dataTypes[0]!=="*"?", */*; q=0.01":""):e.accepts["*"];for(t in e.headers)u.setRequestHeader(t,e.headers[t]);if(e.beforeSend&&(e.beforeSend.call(f,u,e)===!1||r===2)){u.abort();return!1}for(t in {success:1,error:1,complete:1})u[t](e[t]);o=bN(bI,e,c,u);if(o){u.readyState=1,s&&g.trigger("ajaxSend",[u,e]),e.async&&e.timeout>0&&(p=setTimeout(function(){u.abort("timeout")},e.timeout));try{r=1,o.send(l,v)}catch(y){status<2?v(-1,y):d.error(y)}}else v(-1,"No Transport");return u},param:function(a,c){var e=[],f=function(a,b){b=d.isFunction(b)?b():b,e[e.length]=encodeURIComponent(a)+"="+encodeURIComponent(b)};c===b&&(c=d.ajaxSettings.traditional);if(d.isArray(a)||a.jquery&&!d.isPlainObject(a))d.each(a,function(){f(this.name,this.value)});else for(var g in a)bO(g,a[g],c,f);return e.join("&").replace(bp,"+")}}),d.extend({active:0,lastModified:{},etag:{}});var bR=d.now(),bS=/(\=)\?(&|$)|()\?\?()/i;d.ajaxSetup({jsonp:"callback",jsonpCallback:function(){return d.expando+"_"+bR++}}),d.ajaxPrefilter("json jsonp",function(b,c,e){var f=typeof b.data==="string";if(b.dataTypes[0]==="jsonp"||c.jsonpCallback||c.jsonp!=null||b.jsonp!==!1&&(bS.test(b.url)||f&&bS.test(b.data))){var g,h=b.jsonpCallback=d.isFunction(b.jsonpCallback)?b.jsonpCallback():b.jsonpCallback,i=a[h],j=b.url,k=b.data,l="$1"+h+"$2",m=function(){a[h]=i,g&&d.isFunction(i)&&a[h](g[0])};b.jsonp!==!1&&(j=j.replace(bS,l),b.url===j&&(f&&(k=k.replace(bS,l)),b.data===k&&(j+=(/\?/.test(j)?"&":"?")+b.jsonp+"="+h))),b.url=j,b.data=k,a[h]=function(a){g=[a]},e.then(m,m),b.converters["script json"]=function(){g||d.error(h+" was not called");return g[0]},b.dataTypes[0]="json";return"script"}}),d.ajaxSetup({accepts:{script:"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},contents:{script:/javascript|ecmascript/},converters:{"text script":function(a){d.globalEval(a);return a}}}),d.ajaxPrefilter("script",function(a){a.cache===b&&(a.cache=!1),a.crossDomain&&(a.type="GET",a.global=!1)}),d.ajaxTransport("script",function(a){if(a.crossDomain){var d,e=c.head||c.getElementsByTagName("head")[0]||c.documentElement;return{send:function(f,g){d=c.createElement("script"),d.async="async",a.scriptCharset&&(d.charset=a.scriptCharset),d.src=a.url,d.onload=d.onreadystatechange=function(a,c){if(!d.readyState||/loaded|complete/.test(d.readyState))d.onload=d.onreadystatechange=null,e&&d.parentNode&&e.removeChild(d),d=b,c||g(200,"success")},e.insertBefore(d,e.firstChild)},abort:function(){d&&d.onload(0,1)}}}});var bT=d.now(),bU,bV;d.ajaxSettings.xhr=a.ActiveXObject?function(){return!this.isLocal&&bX()||bY()}:bX,bV=d.ajaxSettings.xhr(),d.support.ajax=!!bV,d.support.cors=bV&&"withCredentials"in bV,bV=b,d.support.ajax&&d.ajaxTransport(function(a){if(!a.crossDomain||d.support.cors){var c;return{send:function(e,f){var g=a.xhr(),h,i;a.username?g.open(a.type,a.url,a.async,a.username,a.password):g.open(a.type,a.url,a.async);if(a.xhrFields)for(i in a.xhrFields)g[i]=a.xhrFields[i];a.mimeType&&g.overrideMimeType&&g.overrideMimeType(a.mimeType),(!a.crossDomain||a.hasContent)&&!e["X-Requested-With"]&&(e["X-Requested-With"]="XMLHttpRequest");try{for(i in e)g.setRequestHeader(i,e[i])}catch(j){}g.send(a.hasContent&&a.data||null),c=function(e,i){var j,k,l,m,n;try{if(c&&(i||g.readyState===4)){c=b,h&&(g.onreadystatechange=d.noop,delete bU[h]);if(i)g.readyState!==4&&g.abort();else{j=g.status,l=g.getAllResponseHeaders(),m={},n=g.responseXML,n&&n.documentElement&&(m.xml=n),m.text=g.responseText;try{k=g.statusText}catch(o){k=""}j||!a.isLocal||a.crossDomain?j===1223&&(j=204):j=m.text?200:404}}}catch(p){i||f(-1,p)}m&&f(j,k,m,l)},a.async&&g.readyState!==4?(bU||(bU={},bW()),h=bT++,g.onreadystatechange=bU[h]=c):c()},abort:function(){c&&c(0,1)}}}});var bZ={},b$=/^(?:toggle|show|hide)$/,b_=/^([+\-]=)?([\d+.\-]+)([a-z%]*)$/i,ca,cb=[["height","marginTop","marginBottom","paddingTop","paddingBottom"],["width","marginLeft","marginRight","paddingLeft","paddingRight"],["opacity"]];d.fn.extend({show:function(a,b,c){var e,f;if(a||a===0)return this.animate(cc("show",3),a,b,c);for(var g=0,h=this.length;g<h;g++)e=this[g],f=e.style.display,!d._data(e,"olddisplay")&&f==="none"&&(f=e.style.display=""),f===""&&d.css(e,"display")==="none"&&d._data(e,"olddisplay",cd(e.nodeName));for(g=0;g<h;g++){e=this[g],f=e.style.display;if(f===""||f==="none")e.style.display=d._data(e,"olddisplay")||""}return this},hide:function(a,b,c){if(a||a===0)return this.animate(cc("hide",3),a,b,c);for(var e=0,f=this.length;e<f;e++){var g=d.css(this[e],"display");g!=="none"&&!d._data(this[e],"olddisplay")&&d._data(this[e],"olddisplay",g)}for(e=0;e<f;e++)this[e].style.display="none";return this},_toggle:d.fn.toggle,toggle:function(a,b,c){var e=typeof a==="boolean";d.isFunction(a)&&d.isFunction(b)?this._toggle.apply(this,arguments):a==null||e?this.each(function(){var b=e?a:d(this).is(":hidden");d(this)[b?"show":"hide"]()}):this.animate(cc("toggle",3),a,b,c);return this},fadeTo:function(a,b,c,d){return this.filter(":hidden").css("opacity",0).show().end().animate({opacity:b},a,c,d)},animate:function(a,b,c,e){var f=d.speed(b,c,e);if(d.isEmptyObject(a))return this.each(f.complete);return this[f.queue===!1?"each":"queue"](function(){var b=d.extend({},f),c,e=this.nodeType===1,g=e&&d(this).is(":hidden"),h=this;for(c in a){var i=d.camelCase(c);c!==i&&(a[i]=a[c],delete a[c],c=i);if(a[c]==="hide"&&g||a[c]==="show"&&!g)return b.complete.call(this);if(e&&(c==="height"||c==="width")){b.overflow=[this.style.overflow,this.style.overflowX,this.style.overflowY];if(d.css(this,"display")==="inline"&&d.css(this,"float")==="none")if(d.support.inlineBlockNeedsLayout){var j=cd(this.nodeName);j==="inline"?this.style.display="inline-block":(this.style.display="inline",this.style.zoom=1)}else this.style.display="inline-block"}d.isArray(a[c])&&((b.specialEasing=b.specialEasing||{})[c]=a[c][1],a[c]=a[c][0])}b.overflow!=null&&(this.style.overflow="hidden"),b.curAnim=d.extend({},a),d.each(a,function(c,e){var f=new d.fx(h,b,c);if(b$.test(e))f[e==="toggle"?g?"show":"hide":e](a);else{var i=b_.exec(e),j=f.cur();if(i){var k=parseFloat(i[2]),l=i[3]||(d.cssNumber[c]?"":"px");l!=="px"&&(d.style(h,c,(k||1)+l),j=(k||1)/f.cur()*j,d.style(h,c,j+l)),i[1]&&(k=(i[1]==="-="?-1:1)*k+j),f.custom(j,k,l)}else f.custom(j,e,"")}});return!0})},stop:function(a,b){var c=d.timers;a&&this.queue([]),this.each(function(){for(var a=c.length-1;a>=0;a--)c[a].elem===this&&(b&&c[a](!0),c.splice(a,1))}),b||this.dequeue();return this}}),d.each({slideDown:cc("show",1),slideUp:cc("hide",1),slideToggle:cc("toggle",1),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"},fadeToggle:{opacity:"toggle"}},function(a,b){d.fn[a]=function(a,c,d){return this.animate(b,a,c,d)}}),d.extend({speed:function(a,b,c){var e=a&&typeof a==="object"?d.extend({},a):{complete:c||!c&&b||d.isFunction(a)&&a,duration:a,easing:c&&b||b&&!d.isFunction(b)&&b};e.duration=d.fx.off?0:typeof e.duration==="number"?e.duration:e.duration in d.fx.speeds?d.fx.speeds[e.duration]:d.fx.speeds._default,e.old=e.complete,e.complete=function(){e.queue!==!1&&d(this).dequeue(),d.isFunction(e.old)&&e.old.call(this)};return e},easing:{linear:function(a,b,c,d){return c+d*a},swing:function(a,b,c,d){return(-Math.cos(a*Math.PI)/2+.5)*d+c}},timers:[],fx:function(a,b,c){this.options=b,this.elem=a,this.prop=c,b.orig||(b.orig={})}}),d.fx.prototype={update:function(){this.options.step&&this.options.step.call(this.elem,this.now,this),(d.fx.step[this.prop]||d.fx.step._default)(this)},cur:function(){if(this.elem[this.prop]!=null&&(!this.elem.style||this.elem.style[this.prop]==null))return this.elem[this.prop];var a,b=d.css(this.elem,this.prop);return isNaN(a=parseFloat(b))?!b||b==="auto"?0:b:a},custom:function(a,b,c){function g(a){return e.step(a)}var e=this,f=d.fx;this.startTime=d.now(),this.start=a,this.end=b,this.unit=c||this.unit||(d.cssNumber[this.prop]?"":"px"),this.now=this.start,this.pos=this.state=0,g.elem=this.elem,g()&&d.timers.push(g)&&!ca&&(ca=setInterval(f.tick,f.interval))},show:function(){this.options.orig[this.prop]=d.style(this.elem,this.prop),this.options.show=!0,this.custom(this.prop==="width"||this.prop==="height"?1:0,this.cur()),d(this.elem).show()},hide:function(){this.options.orig[this.prop]=d.style(this.elem,this.prop),this.options.hide=!0,this.custom(this.cur(),0)},step:function(a){var b=d.now(),c=!0;if(a||b>=this.options.duration+this.startTime){this.now=this.end,this.pos=this.state=1,this.update(),this.options.curAnim[this.prop]=!0;for(var e in this.options.curAnim)this.options.curAnim[e]!==!0&&(c=!1);if(c){if(this.options.overflow!=null&&!d.support.shrinkWrapBlocks){var f=this.elem,g=this.options;d.each(["","X","Y"],function(a,b){f.style["overflow"+b]=g.overflow[a]})}this.options.hide&&d(this.elem).hide();if(this.options.hide||this.options.show)for(var h in this.options.curAnim)d.style(this.elem,h,this.options.orig[h]);this.options.complete.call(this.elem)}return!1}var i=b-this.startTime;this.state=i/this.options.duration;var j=this.options.specialEasing&&this.options.specialEasing[this.prop],k=this.options.easing||(d.easing.swing?"swing":"linear");this.pos=d.easing[j||k](this.state,i,0,1,this.options.duration),this.now=this.start+(this.end-this.start)*this.pos,this.update();return!0}},d.extend(d.fx,{tick:function(){var a=d.timers;for(var b=0;b<a.length;b++)a[b]()||a.splice(b--,1);a.length||d.fx.stop()},interval:13,stop:function(){clearInterval(ca),ca=null},speeds:{slow:600,fast:200,_default:400},step:{opacity:function(a){d.style(a.elem,"opacity",a.now)},_default:function(a){a.elem.style&&a.elem.style[a.prop]!=null?a.elem.style[a.prop]=(a.prop==="width"||a.prop==="height"?Math.max(0,a.now):a.now)+a.unit:a.elem[a.prop]=a.now}}}),d.expr&&d.expr.filters&&(d.expr.filters.animated=function(a){return d.grep(d.timers,function(b){return a===b.elem}).length});var ce=/^t(?:able|d|h)$/i,cf=/^(?:body|html)$/i;"getBoundingClientRect"in c.documentElement?d.fn.offset=function(a){var b=this[0],c;if(a)return this.each(function(b){d.offset.setOffset(this,a,b)});if(!b||!b.ownerDocument)return null;if(b===b.ownerDocument.body)return d.offset.bodyOffset(b);try{c=b.getBoundingClientRect()}catch(e){}var f=b.ownerDocument,g=f.documentElement;if(!c||!d.contains(g,b))return c?{top:c.top,left:c.left}:{top:0,left:0};var h=f.body,i=cg(f),j=g.clientTop||h.clientTop||0,k=g.clientLeft||h.clientLeft||0,l=i.pageYOffset||d.support.boxModel&&g.scrollTop||h.scrollTop,m=i.pageXOffset||d.support.boxModel&&g.scrollLeft||h.scrollLeft,n=c.top+l-j,o=c.left+m-k;return{top:n,left:o}}:d.fn.offset=function(a){var b=this[0];if(a)return this.each(function(b){d.offset.setOffset(this,a,b)});if(!b||!b.ownerDocument)return null;if(b===b.ownerDocument.body)return d.offset.bodyOffset(b);d.offset.initialize();var c,e=b.offsetParent,f=b,g=b.ownerDocument,h=g.documentElement,i=g.body,j=g.defaultView,k=j?j.getComputedStyle(b,null):b.currentStyle,l=b.offsetTop,m=b.offsetLeft;while((b=b.parentNode)&&b!==i&&b!==h){if(d.offset.supportsFixedPosition&&k.position==="fixed")break;c=j?j.getComputedStyle(b,null):b.currentStyle,l-=b.scrollTop,m-=b.scrollLeft,b===e&&(l+=b.offsetTop,m+=b.offsetLeft,d.offset.doesNotAddBorder&&(!d.offset.doesAddBorderForTableAndCells||!ce.test(b.nodeName))&&(l+=parseFloat(c.borderTopWidth)||0,m+=parseFloat(c.borderLeftWidth)||0),f=e,e=b.offsetParent),d.offset.subtractsBorderForOverflowNotVisible&&c.overflow!=="visible"&&(l+=parseFloat(c.borderTopWidth)||0,m+=parseFloat(c.borderLeftWidth)||0),k=c}if(k.position==="relative"||k.position==="static")l+=i.offsetTop,m+=i.offsetLeft;d.offset.supportsFixedPosition&&k.position==="fixed"&&(l+=Math.max(h.scrollTop,i.scrollTop),m+=Math.max(h.scrollLeft,i.scrollLeft));return{top:l,left:m}},d.offset={initialize:function(){var a=c.body,b=c.createElement("div"),e,f,g,h,i=parseFloat(d.css(a,"marginTop"))||0,j="<div style='position:absolute;top:0;left:0;margin:0;border:5px solid #000;padding:0;width:1px;height:1px;'><div></div></div><table style='position:absolute;top:0;left:0;margin:0;border:5px solid #000;padding:0;width:1px;height:1px;' cellpadding='0' cellspacing='0'><tr><td></td></tr></table>";d.extend(b.style,{position:"absolute",top:0,left:0,margin:0,border:0,width:"1px",height:"1px",visibility:"hidden"}),b.innerHTML=j,a.insertBefore(b,a.firstChild),e=b.firstChild,f=e.firstChild,h=e.nextSibling.firstChild.firstChild,this.doesNotAddBorder=f.offsetTop!==5,this.doesAddBorderForTableAndCells=h.offsetTop===5,f.style.position="fixed",f.style.top="20px",this.supportsFixedPosition=f.offsetTop===20||f.offsetTop===15,f.style.position=f.style.top="",e.style.overflow="hidden",e.style.position="relative",this.subtractsBorderForOverflowNotVisible=f.offsetTop===-5,this.doesNotIncludeMarginInBodyOffset=a.offsetTop!==i,a.removeChild(b),a=b=e=f=g=h=null,d.offset.initialize=d.noop},bodyOffset:function(a){var b=a.offsetTop,c=a.offsetLeft;d.offset.initialize(),d.offset.doesNotIncludeMarginInBodyOffset&&(b+=parseFloat(d.css(a,"marginTop"))||0,c+=parseFloat(d.css(a,"marginLeft"))||0);return{top:b,left:c}},setOffset:function(a,b,c){var e=d.css(a,"position");e==="static"&&(a.style.position="relative");var f=d(a),g=f.offset(),h=d.css(a,"top"),i=d.css(a,"left"),j=e==="absolute"&&d.inArray("auto",[h,i])>-1,k={},l={},m,n;j&&(l=f.position()),m=j?l.top:parseInt(h,10)||0,n=j?l.left:parseInt(i,10)||0,d.isFunction(b)&&(b=b.call(a,c,g)),b.top!=null&&(k.top=b.top-g.top+m),b.left!=null&&(k.left=b.left-g.left+n),"using"in b?b.using.call(a,k):f.css(k)}},d.fn.extend({position:function(){if(!this[0])return null;var a=this[0],b=this.offsetParent(),c=this.offset(),e=cf.test(b[0].nodeName)?{top:0,left:0}:b.offset();c.top-=parseFloat(d.css(a,"marginTop"))||0,c.left-=parseFloat(d.css(a,"marginLeft"))||0,e.top+=parseFloat(d.css(b[0],"borderTopWidth"))||0,e.left+=parseFloat(d.css(b[0],"borderLeftWidth"))||0;return{top:c.top-e.top,left:c.left-e.left}},offsetParent:function(){return this.map(function(){var a=this.offsetParent||c.body;while(a&&(!cf.test(a.nodeName)&&d.css(a,"position")==="static"))a=a.offsetParent;return a})}}),d.each(["Left","Top"],function(a,c){var e="scroll"+c;d.fn[e]=function(c){var f=this[0],g;if(!f)return null;if(c!==b)return this.each(function(){g=cg(this),g?g.scrollTo(a?d(g).scrollLeft():c,a?c:d(g).scrollTop()):this[e]=c});g=cg(f);return g?"pageXOffset"in g?g[a?"pageYOffset":"pageXOffset"]:d.support.boxModel&&g.document.documentElement[e]||g.document.body[e]:f[e]}}),d.each(["Height","Width"],function(a,c){var e=c.toLowerCase();d.fn["inner"+c]=function(){return this[0]?parseFloat(d.css(this[0],e,"padding")):null},d.fn["outer"+c]=function(a){return this[0]?parseFloat(d.css(this[0],e,a?"margin":"border")):null},d.fn[e]=function(a){var f=this[0];if(!f)return a==null?null:this;if(d.isFunction(a))return this.each(function(b){var c=d(this);c[e](a.call(this,b,c[e]()))});if(d.isWindow(f)){var g=f.document.documentElement["client"+c];return f.document.compatMode==="CSS1Compat"&&g||f.document.body["client"+c]||g}if(f.nodeType===9)return Math.max(f.documentElement["client"+c],f.body["scroll"+c],f.documentElement["scroll"+c],f.body["offset"+c],f.documentElement["offset"+c]);if(a===b){var h=d.css(f,e),i=parseFloat(h);return d.isNaN(i)?h:i}return this.css(e,typeof a==="string"?a:a+"px")}}),a.jQuery=a.$=d})(window);
/*!
 * jQuery Templates Plugin 1.0.0pre
 * http://github.com/jquery/jquery-tmpl
 * Requires jQuery 1.4.2
 *
 * Copyright Software Freedom Conservancy, Inc.
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 */
(function( jQuery, undefined ){
	var oldManip = jQuery.fn.domManip, tmplItmAtt = "_tmplitem", htmlExpr = /^[^<]*(<[\w\W]+>)[^>]*$|\{\{\! /,
		newTmplItems = {}, wrappedItems = {}, appendToTmplItems, topTmplItem = { key: 0, data: {} }, itemKey = 0, cloneIndex = 0, stack = [];

	function newTmplItem( options, parentItem, fn, data ) {
		// Returns a template item data structure for a new rendered instance of a template (a 'template item').
		// The content field is a hierarchical array of strings and nested items (to be
		// removed and replaced by nodes field of dom elements, once inserted in DOM).
		var newItem = {
			data: data || (data === 0 || data === false) ? data : (parentItem ? parentItem.data : {}),
			_wrap: parentItem ? parentItem._wrap : null,
			tmpl: null,
			parent: parentItem || null,
			nodes: [],
			calls: tiCalls,
			nest: tiNest,
			wrap: tiWrap,
			html: tiHtml,
			update: tiUpdate
		};
		if ( options ) {
			jQuery.extend( newItem, options, { nodes: [], parent: parentItem });
		}
		if ( fn ) {
			// Build the hierarchical content to be used during insertion into DOM
			newItem.tmpl = fn;
			newItem._ctnt = newItem._ctnt || newItem.tmpl( jQuery, newItem );
			newItem.key = ++itemKey;
			// Keep track of new template item, until it is stored as jQuery Data on DOM element
			(stack.length ? wrappedItems : newTmplItems)[itemKey] = newItem;
		}
		return newItem;
	}

	// Override appendTo etc., in order to provide support for targeting multiple elements. (This code would disappear if integrated in jquery core).
	jQuery.each({
		appendTo: "append",
		prependTo: "prepend",
		insertBefore: "before",
		insertAfter: "after",
		replaceAll: "replaceWith"
	}, function( name, original ) {
		jQuery.fn[ name ] = function( selector ) {
			var ret = [], insert = jQuery( selector ), elems, i, l, tmplItems,
				parent = this.length === 1 && this[0].parentNode;

			appendToTmplItems = newTmplItems || {};
			if ( parent && parent.nodeType === 11 && parent.childNodes.length === 1 && insert.length === 1 ) {
				insert[ original ]( this[0] );
				ret = this;
			} else {
				for ( i = 0, l = insert.length; i < l; i++ ) {
					cloneIndex = i;
					elems = (i > 0 ? this.clone(true) : this).get();
					jQuery( insert[i] )[ original ]( elems );
					ret = ret.concat( elems );
				}
				cloneIndex = 0;
				ret = this.pushStack( ret, name, insert.selector );
			}
			tmplItems = appendToTmplItems;
			appendToTmplItems = null;
			jQuery.tmpl.complete( tmplItems );
			return ret;
		};
	});

	jQuery.fn.extend({
		// Use first wrapped element as template markup.
		// Return wrapped set of template items, obtained by rendering template against data.
		tmpl: function( data, options, parentItem ) {
			return jQuery.tmpl( this[0], data, options, parentItem );
		},

		// Find which rendered template item the first wrapped DOM element belongs to
		tmplItem: function() {
			return jQuery.tmplItem( this[0] );
		},

		// Consider the first wrapped element as a template declaration, and get the compiled template or store it as a named template.
		template: function( name ) {
			return jQuery.template( name, this[0] );
		},

		domManip: function( args, table, callback, options ) {
			if ( args[0] && jQuery.isArray( args[0] )) {
				var dmArgs = jQuery.makeArray( arguments ), elems = args[0], elemsLength = elems.length, i = 0, tmplItem;
				while ( i < elemsLength && !(tmplItem = jQuery.data( elems[i++], "tmplItem" ))) {}
				if ( tmplItem && cloneIndex ) {
					dmArgs[2] = function( fragClone ) {
						// Handler called by oldManip when rendered template has been inserted into DOM.
						jQuery.tmpl.afterManip( this, fragClone, callback );
					};
				}
				oldManip.apply( this, dmArgs );
			} else {
				oldManip.apply( this, arguments );
			}
			cloneIndex = 0;
			if ( !appendToTmplItems ) {
				jQuery.tmpl.complete( newTmplItems );
			}
			return this;
		}
	});

	jQuery.extend({
		// Return wrapped set of template items, obtained by rendering template against data.
		tmpl: function( tmpl, data, options, parentItem ) {
			var ret, topLevel = !parentItem;
			if ( topLevel ) {
				// This is a top-level tmpl call (not from a nested template using {{tmpl}})
				parentItem = topTmplItem;
				tmpl = jQuery.template[tmpl] || jQuery.template( null, tmpl );
				wrappedItems = {}; // Any wrapped items will be rebuilt, since this is top level
			} else if ( !tmpl ) {
				// The template item is already associated with DOM - this is a refresh.
				// Re-evaluate rendered template for the parentItem
				tmpl = parentItem.tmpl;
				newTmplItems[parentItem.key] = parentItem;
				parentItem.nodes = [];
				if ( parentItem.wrapped ) {
					updateWrapped( parentItem, parentItem.wrapped );
				}
				// Rebuild, without creating a new template item
				return jQuery( build( parentItem, null, parentItem.tmpl( jQuery, parentItem ) ));
			}
			if ( !tmpl ) {
				return []; // Could throw...
			}
			if ( typeof data === "function" ) {
				data = data.call( parentItem || {} );
			}
			if ( options && options.wrapped ) {
				updateWrapped( options, options.wrapped );
			}
			ret = jQuery.isArray( data ) ?
				jQuery.map( data, function( dataItem ) {
					return dataItem ? newTmplItem( options, parentItem, tmpl, dataItem ) : null;
				}) :
				[ newTmplItem( options, parentItem, tmpl, data ) ];
			return topLevel ? jQuery( build( parentItem, null, ret ) ) : ret;
		},

		// Return rendered template item for an element.
		tmplItem: function( elem ) {
			var tmplItem;
			if ( elem instanceof jQuery ) {
				elem = elem[0];
			}
			while ( elem && elem.nodeType === 1 && !(tmplItem = jQuery.data( elem, "tmplItem" )) && (elem = elem.parentNode) ) {}
			return tmplItem || topTmplItem;
		},

		// Set:
		// Use $.template( name, tmpl ) to cache a named template,
		// where tmpl is a template string, a script element or a jQuery instance wrapping a script element, etc.
		// Use $( "selector" ).template( name ) to provide access by name to a script block template declaration.

		// Get:
		// Use $.template( name ) to access a cached template.
		// Also $( selectorToScriptBlock ).template(), or $.template( null, templateString )
		// will return the compiled template, without adding a name reference.
		// If templateString includes at least one HTML tag, $.template( templateString ) is equivalent
		// to $.template( null, templateString )
		template: function( name, tmpl ) {
			if (tmpl) {
				// Compile template and associate with name
				if ( typeof tmpl === "string" ) {
					// This is an HTML string being passed directly in.
					tmpl = buildTmplFn( tmpl );
				} else if ( tmpl instanceof jQuery ) {
					tmpl = tmpl[0] || {};
				}
				if ( tmpl.nodeType ) {
					// If this is a template block, use cached copy, or generate tmpl function and cache.
					tmpl = jQuery.data( tmpl, "tmpl" ) || jQuery.data( tmpl, "tmpl", buildTmplFn( tmpl.innerHTML ));
					// Issue: In IE, if the container element is not a script block, the innerHTML will remove quotes from attribute values whenever the value does not include white space.
					// This means that foo="${x}" will not work if the value of x includes white space: foo="${x}" -> foo=value of x.
					// To correct this, include space in tag: foo="${ x }" -> foo="value of x"
				}
				return typeof name === "string" ? (jQuery.template[name] = tmpl) : tmpl;
			}
			// Return named compiled template
			return name ? (typeof name !== "string" ? jQuery.template( null, name ):
				(jQuery.template[name] ||
					// If not in map, and not containing at least on HTML tag, treat as a selector.
					// (If integrated with core, use quickExpr.exec)
					jQuery.template( null, htmlExpr.test( name ) ? name : jQuery( name )))) : null;
		},

		encode: function( text ) {
			// Do HTML encoding replacing < > & and ' and " by corresponding entities.
			return ("" + text).split("<").join("&lt;").split(">").join("&gt;").split('"').join("&#34;").split("'").join("&#39;");
		}
	});

	jQuery.extend( jQuery.tmpl, {
		tag: {
			"tmpl": {
				_default: { $2: "null" },
				open: "if($notnull_1){__=__.concat($item.nest($1,$2));}"
				// tmpl target parameter can be of type function, so use $1, not $1a (so not auto detection of functions)
				// This means that {{tmpl foo}} treats foo as a template (which IS a function).
				// Explicit parens can be used if foo is a function that returns a template: {{tmpl foo()}}.
			},
			"wrap": {
				_default: { $2: "null" },
				open: "$item.calls(__,$1,$2);__=[];",
				close: "call=$item.calls();__=call._.concat($item.wrap(call,__));"
			},
			"each": {
				_default: { $2: "$index, $value" },
				open: "if($notnull_1){$.each($1a,function($2){with(this){",
				close: "}});}"
			},
			"if": {
				open: "if(($notnull_1) && $1a){",
				close: "}"
			},
			"else": {
				_default: { $1: "true" },
				open: "}else if(($notnull_1) && $1a){"
			},
			"html": {
				// Unecoded expression evaluation.
				open: "if($notnull_1){__.push($1a);}"
			},
			"=": {
				// Encoded expression evaluation. Abbreviated form is ${}.
				_default: { $1: "$data" },
				open: "if($notnull_1){__.push($.encode($1a));}"
			},
			"!": {
				// Comment tag. Skipped by parser
				open: ""
			}
		},

		// This stub can be overridden, e.g. in jquery.tmplPlus for providing rendered events
		complete: function( items ) {
			newTmplItems = {};
		},

		// Call this from code which overrides domManip, or equivalent
		// Manage cloning/storing template items etc.
		afterManip: function afterManip( elem, fragClone, callback ) {
			// Provides cloned fragment ready for fixup prior to and after insertion into DOM
			var content = fragClone.nodeType === 11 ?
				jQuery.makeArray(fragClone.childNodes) :
				fragClone.nodeType === 1 ? [fragClone] : [];

			// Return fragment to original caller (e.g. append) for DOM insertion
			callback.call( elem, fragClone );

			// Fragment has been inserted:- Add inserted nodes to tmplItem data structure. Replace inserted element annotations by jQuery.data.
			storeTmplItems( content );
			cloneIndex++;
		}
	});

	//========================== Private helper functions, used by code above ==========================

	function build( tmplItem, nested, content ) {
		// Convert hierarchical content into flat string array
		// and finally return array of fragments ready for DOM insertion
		var frag, ret = content ? jQuery.map( content, function( item ) {
			return (typeof item === "string") ?
				// Insert template item annotations, to be converted to jQuery.data( "tmplItem" ) when elems are inserted into DOM.
				(tmplItem.key ? item.replace( /(<\w+)(?=[\s>])(?![^>]*_tmplitem)([^>]*)/g, "$1 " + tmplItmAtt + "=\"" + tmplItem.key + "\" $2" ) : item) :
				// This is a child template item. Build nested template.
				build( item, tmplItem, item._ctnt );
		}) :
		// If content is not defined, insert tmplItem directly. Not a template item. May be a string, or a string array, e.g. from {{html $item.html()}}.
		tmplItem;
		if ( nested ) {
			return ret;
		}

		// top-level template
		ret = ret.join("");

		// Support templates which have initial or final text nodes, or consist only of text
		// Also support HTML entities within the HTML markup.
		ret.replace( /^\s*([^<\s][^<]*)?(<[\w\W]+>)([^>]*[^>\s])?\s*$/, function( all, before, middle, after) {
			frag = jQuery( middle ).get();

			storeTmplItems( frag );
			if ( before ) {
				frag = unencode( before ).concat(frag);
			}
			if ( after ) {
				frag = frag.concat(unencode( after ));
			}
		});
		return frag ? frag : unencode( ret );
	}

	function unencode( text ) {
		// Use createElement, since createTextNode will not render HTML entities correctly
		var el = document.createElement( "div" );
		el.innerHTML = text;
		return jQuery.makeArray(el.childNodes);
	}

	// Generate a reusable function that will serve to render a template against data
	function buildTmplFn( markup ) {
		return new Function("jQuery","$item",
			// Use the variable __ to hold a string array while building the compiled template. (See https://github.com/jquery/jquery-tmpl/issues#issue/10).
			"var $=jQuery,call,__=[],$data=$item.data;" +

			// Introduce the data as local variables using with(){}
			"with($data){__.push('" +

			// Convert the template into pure JavaScript
			jQuery.trim(markup)
				.replace( /([\\'])/g, "\\$1" )
				.replace( /[\r\t\n]/g, " " )
				.replace( /\$\{([^\}]*)\}/g, "{{= $1}}" )
				.replace( /\{\{(\/?)(\w+|.)(?:\(((?:[^\}]|\}(?!\}))*?)?\))?(?:\s+(.*?)?)?(\(((?:[^\}]|\}(?!\}))*?)\))?\s*\}\}/g,
				function( all, slash, type, fnargs, target, parens, args ) {
					var tag = jQuery.tmpl.tag[ type ], def, expr, exprAutoFnDetect;
					if ( !tag ) {
						throw "Unknown template tag: " + type;
					}
					def = tag._default || [];
					if ( parens && !/\w$/.test(target)) {
						target += parens;
						parens = "";
					}
					if ( target ) {
						target = unescape( target );
						args = args ? ("," + unescape( args ) + ")") : (parens ? ")" : "");
						// Support for target being things like a.toLowerCase();
						// In that case don't call with template item as 'this' pointer. Just evaluate...
						expr = parens ? (target.indexOf(".") > -1 ? target + unescape( parens ) : ("(" + target + ").call($item" + args)) : target;
						exprAutoFnDetect = parens ? expr : "(typeof(" + target + ")==='function'?(" + target + ").call($item):(" + target + "))";
					} else {
						exprAutoFnDetect = expr = def.$1 || "null";
					}
					fnargs = unescape( fnargs );
					return "');" +
						tag[ slash ? "close" : "open" ]
							.split( "$notnull_1" ).join( target ? "typeof(" + target + ")!=='undefined' && (" + target + ")!=null" : "true" )
							.split( "$1a" ).join( exprAutoFnDetect )
							.split( "$1" ).join( expr )
							.split( "$2" ).join( fnargs || def.$2 || "" ) +
						"__.push('";
				}) +
			"');}return __;"
		);
	}
	function updateWrapped( options, wrapped ) {
		// Build the wrapped content.
		options._wrap = build( options, true,
			// Suport imperative scenario in which options.wrapped can be set to a selector or an HTML string.
			jQuery.isArray( wrapped ) ? wrapped : [htmlExpr.test( wrapped ) ? wrapped : jQuery( wrapped ).html()]
		).join("");
	}

	function unescape( args ) {
		return args ? args.replace( /\\'/g, "'").replace(/\\\\/g, "\\" ) : null;
	}
	function outerHtml( elem ) {
		var div = document.createElement("div");
		div.appendChild( elem.cloneNode(true) );
		return div.innerHTML;
	}

	// Store template items in jQuery.data(), ensuring a unique tmplItem data data structure for each rendered template instance.
	function storeTmplItems( content ) {
		var keySuffix = "_" + cloneIndex, elem, elems, newClonedItems = {}, i, l, m;
		for ( i = 0, l = content.length; i < l; i++ ) {
			if ( (elem = content[i]).nodeType !== 1 ) {
				continue;
			}
			elems = elem.getElementsByTagName("*");
			for ( m = elems.length - 1; m >= 0; m-- ) {
				processItemKey( elems[m] );
			}
			processItemKey( elem );
		}
		function processItemKey( el ) {
			var pntKey, pntNode = el, pntItem, tmplItem, key;
			// Ensure that each rendered template inserted into the DOM has its own template item,
			if ( (key = el.getAttribute( tmplItmAtt ))) {
				while ( pntNode.parentNode && (pntNode = pntNode.parentNode).nodeType === 1 && !(pntKey = pntNode.getAttribute( tmplItmAtt ))) { }
				if ( pntKey !== key ) {
					// The next ancestor with a _tmplitem expando is on a different key than this one.
					// So this is a top-level element within this template item
					// Set pntNode to the key of the parentNode, or to 0 if pntNode.parentNode is null, or pntNode is a fragment.
					pntNode = pntNode.parentNode ? (pntNode.nodeType === 11 ? 0 : (pntNode.getAttribute( tmplItmAtt ) || 0)) : 0;
					if ( !(tmplItem = newTmplItems[key]) ) {
						// The item is for wrapped content, and was copied from the temporary parent wrappedItem.
						tmplItem = wrappedItems[key];
						tmplItem = newTmplItem( tmplItem, newTmplItems[pntNode]||wrappedItems[pntNode] );
						tmplItem.key = ++itemKey;
						newTmplItems[itemKey] = tmplItem;
					}
					if ( cloneIndex ) {
						cloneTmplItem( key );
					}
				}
				el.removeAttribute( tmplItmAtt );
			} else if ( cloneIndex && (tmplItem = jQuery.data( el, "tmplItem" )) ) {
				// This was a rendered element, cloned during append or appendTo etc.
				// TmplItem stored in jQuery data has already been cloned in cloneCopyEvent. We must replace it with a fresh cloned tmplItem.
				cloneTmplItem( tmplItem.key );
				newTmplItems[tmplItem.key] = tmplItem;
				pntNode = jQuery.data( el.parentNode, "tmplItem" );
				pntNode = pntNode ? pntNode.key : 0;
			}
			if ( tmplItem ) {
				pntItem = tmplItem;
				// Find the template item of the parent element.
				// (Using !=, not !==, since pntItem.key is number, and pntNode may be a string)
				while ( pntItem && pntItem.key != pntNode ) {
					// Add this element as a top-level node for this rendered template item, as well as for any
					// ancestor items between this item and the item of its parent element
					pntItem.nodes.push( el );
					pntItem = pntItem.parent;
				}
				// Delete content built during rendering - reduce API surface area and memory use, and avoid exposing of stale data after rendering...
				delete tmplItem._ctnt;
				delete tmplItem._wrap;
				// Store template item as jQuery data on the element
				jQuery.data( el, "tmplItem", tmplItem );
			}
			function cloneTmplItem( key ) {
				key = key + keySuffix;
				tmplItem = newClonedItems[key] =
					(newClonedItems[key] || newTmplItem( tmplItem, newTmplItems[tmplItem.parent.key + keySuffix] || tmplItem.parent ));
			}
		}
	}

	//---- Helper functions for template item ----

	function tiCalls( content, tmpl, data, options ) {
		if ( !content ) {
			return stack.pop();
		}
		stack.push({ _: content, tmpl: tmpl, item:this, data: data, options: options });
	}

	function tiNest( tmpl, data, options ) {
		// nested template, using {{tmpl}} tag
		return jQuery.tmpl( jQuery.template( tmpl ), data, options, this );
	}

	function tiWrap( call, wrapped ) {
		// nested template, using {{wrap}} tag
		var options = call.options || {};
		options.wrapped = wrapped;
		// Apply the template, which may incorporate wrapped content,
		return jQuery.tmpl( jQuery.template( call.tmpl ), call.data, options, call.item );
	}

	function tiHtml( filter, textOnly ) {
		var wrapped = this._wrap;
		return jQuery.map(
			jQuery( jQuery.isArray( wrapped ) ? wrapped.join("") : wrapped ).filter( filter || "*" ),
			function(e) {
				return textOnly ?
					e.innerText || e.textContent :
					e.outerHTML || outerHtml(e);
			});
	}

	function tiUpdate() {
		var coll = this.nodes;
		jQuery.tmpl( null, null, null, this).insertBefore( coll[0] );
		jQuery( coll ).remove();
	}
})( jQuery );

/*!
 * jQuery UI 1.8.11
 *
 * Copyright 2011, AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://jquery.org/license
 *
 * http://docs.jquery.com/UI
 */
(function(b,d){function e(g){return!b(g).parents().andSelf().filter(function(){return b.curCSS(this,"visibility")==="hidden"||b.expr.filters.hidden(this)}).length}b.ui=b.ui||{};if(!b.ui.version){b.extend(b.ui,{version:"1.8.11",keyCode:{ALT:18,BACKSPACE:8,CAPS_LOCK:20,COMMA:188,COMMAND:91,COMMAND_LEFT:91,COMMAND_RIGHT:93,CONTROL:17,DELETE:46,DOWN:40,END:35,ENTER:13,ESCAPE:27,HOME:36,INSERT:45,LEFT:37,MENU:93,NUMPAD_ADD:107,NUMPAD_DECIMAL:110,NUMPAD_DIVIDE:111,NUMPAD_ENTER:108,NUMPAD_MULTIPLY:106,
NUMPAD_SUBTRACT:109,PAGE_DOWN:34,PAGE_UP:33,PERIOD:190,RIGHT:39,SHIFT:16,SPACE:32,TAB:9,UP:38,WINDOWS:91}});b.fn.extend({_focus:b.fn.focus,focus:function(g,f){return typeof g==="number"?this.each(function(){var a=this;setTimeout(function(){b(a).focus();f&&f.call(a)},g)}):this._focus.apply(this,arguments)},scrollParent:function(){var g;g=b.browser.msie&&/(static|relative)/.test(this.css("position"))||/absolute/.test(this.css("position"))?this.parents().filter(function(){return/(relative|absolute|fixed)/.test(b.curCSS(this,
"position",1))&&/(auto|scroll)/.test(b.curCSS(this,"overflow",1)+b.curCSS(this,"overflow-y",1)+b.curCSS(this,"overflow-x",1))}).eq(0):this.parents().filter(function(){return/(auto|scroll)/.test(b.curCSS(this,"overflow",1)+b.curCSS(this,"overflow-y",1)+b.curCSS(this,"overflow-x",1))}).eq(0);return/fixed/.test(this.css("position"))||!g.length?b(document):g},zIndex:function(g){if(g!==d)return this.css("zIndex",g);if(this.length){g=b(this[0]);for(var f;g.length&&g[0]!==document;){f=g.css("position");
if(f==="absolute"||f==="relative"||f==="fixed"){f=parseInt(g.css("zIndex"),10);if(!isNaN(f)&&f!==0)return f}g=g.parent()}}return 0},disableSelection:function(){return this.bind((b.support.selectstart?"selectstart":"mousedown")+".ui-disableSelection",function(g){g.preventDefault()})},enableSelection:function(){return this.unbind(".ui-disableSelection")}});b.each(["Width","Height"],function(g,f){function a(j,n,p,l){b.each(c,function(){n-=parseFloat(b.curCSS(j,"padding"+this,true))||0;if(p)n-=parseFloat(b.curCSS(j,
"border"+this+"Width",true))||0;if(l)n-=parseFloat(b.curCSS(j,"margin"+this,true))||0});return n}var c=f==="Width"?["Left","Right"]:["Top","Bottom"],h=f.toLowerCase(),i={innerWidth:b.fn.innerWidth,innerHeight:b.fn.innerHeight,outerWidth:b.fn.outerWidth,outerHeight:b.fn.outerHeight};b.fn["inner"+f]=function(j){if(j===d)return i["inner"+f].call(this);return this.each(function(){b(this).css(h,a(this,j)+"px")})};b.fn["outer"+f]=function(j,n){if(typeof j!=="number")return i["outer"+f].call(this,j);return this.each(function(){b(this).css(h,
a(this,j,true,n)+"px")})}});b.extend(b.expr[":"],{data:function(g,f,a){return!!b.data(g,a[3])},focusable:function(g){var f=g.nodeName.toLowerCase(),a=b.attr(g,"tabindex");if("area"===f){f=g.parentNode;a=f.name;if(!g.href||!a||f.nodeName.toLowerCase()!=="map")return false;g=b("img[usemap=#"+a+"]")[0];return!!g&&e(g)}return(/input|select|textarea|button|object/.test(f)?!g.disabled:"a"==f?g.href||!isNaN(a):!isNaN(a))&&e(g)},tabbable:function(g){var f=b.attr(g,"tabindex");return(isNaN(f)||f>=0)&&b(g).is(":focusable")}});
b(function(){var g=document.body,f=g.appendChild(f=document.createElement("div"));b.extend(f.style,{minHeight:"100px",height:"auto",padding:0,borderWidth:0});b.support.minHeight=f.offsetHeight===100;b.support.selectstart="onselectstart"in f;g.removeChild(f).style.display="none"});b.extend(b.ui,{plugin:{add:function(g,f,a){g=b.ui[g].prototype;for(var c in a){g.plugins[c]=g.plugins[c]||[];g.plugins[c].push([f,a[c]])}},call:function(g,f,a){if((f=g.plugins[f])&&g.element[0].parentNode)for(var c=0;c<f.length;c++)g.options[f[c][0]]&&
f[c][1].apply(g.element,a)}},contains:function(g,f){return document.compareDocumentPosition?g.compareDocumentPosition(f)&16:g!==f&&g.contains(f)},hasScroll:function(g,f){if(b(g).css("overflow")==="hidden")return false;f=f&&f==="left"?"scrollLeft":"scrollTop";var a=false;if(g[f]>0)return true;g[f]=1;a=g[f]>0;g[f]=0;return a},isOverAxis:function(g,f,a){return g>f&&g<f+a},isOver:function(g,f,a,c,h,i){return b.ui.isOverAxis(g,a,h)&&b.ui.isOverAxis(f,c,i)}})}})(jQuery);
(function(b,d){if(b.cleanData){var e=b.cleanData;b.cleanData=function(f){for(var a=0,c;(c=f[a])!=null;a++)b(c).triggerHandler("remove");e(f)}}else{var g=b.fn.remove;b.fn.remove=function(f,a){return this.each(function(){if(!a)if(!f||b.filter(f,[this]).length)b("*",this).add([this]).each(function(){b(this).triggerHandler("remove")});return g.call(b(this),f,a)})}}b.widget=function(f,a,c){var h=f.split(".")[0],i;f=f.split(".")[1];i=h+"-"+f;if(!c){c=a;a=b.Widget}b.expr[":"][i]=function(j){return!!b.data(j,
f)};b[h]=b[h]||{};b[h][f]=function(j,n){arguments.length&&this._createWidget(j,n)};a=new a;a.options=b.extend(true,{},a.options);b[h][f].prototype=b.extend(true,a,{namespace:h,widgetName:f,widgetEventPrefix:b[h][f].prototype.widgetEventPrefix||f,widgetBaseClass:i},c);b.widget.bridge(f,b[h][f])};b.widget.bridge=function(f,a){b.fn[f]=function(c){var h=typeof c==="string",i=Array.prototype.slice.call(arguments,1),j=this;c=!h&&i.length?b.extend.apply(null,[true,c].concat(i)):c;if(h&&c.charAt(0)==="_")return j;
h?this.each(function(){var n=b.data(this,f),p=n&&b.isFunction(n[c])?n[c].apply(n,i):n;if(p!==n&&p!==d){j=p;return false}}):this.each(function(){var n=b.data(this,f);n?n.option(c||{})._init():b.data(this,f,new a(c,this))});return j}};b.Widget=function(f,a){arguments.length&&this._createWidget(f,a)};b.Widget.prototype={widgetName:"widget",widgetEventPrefix:"",options:{disabled:false},_createWidget:function(f,a){b.data(a,this.widgetName,this);this.element=b(a);this.options=b.extend(true,{},this.options,
this._getCreateOptions(),f);var c=this;this.element.bind("remove."+this.widgetName,function(){c.destroy()});this._create();this._trigger("create");this._init()},_getCreateOptions:function(){return b.metadata&&b.metadata.get(this.element[0])[this.widgetName]},_create:function(){},_init:function(){},destroy:function(){this.element.unbind("."+this.widgetName).removeData(this.widgetName);this.widget().unbind("."+this.widgetName).removeAttr("aria-disabled").removeClass(this.widgetBaseClass+"-disabled ui-state-disabled")},
widget:function(){return this.element},option:function(f,a){var c=f;if(arguments.length===0)return b.extend({},this.options);if(typeof f==="string"){if(a===d)return this.options[f];c={};c[f]=a}this._setOptions(c);return this},_setOptions:function(f){var a=this;b.each(f,function(c,h){a._setOption(c,h)});return this},_setOption:function(f,a){this.options[f]=a;if(f==="disabled")this.widget()[a?"addClass":"removeClass"](this.widgetBaseClass+"-disabled ui-state-disabled").attr("aria-disabled",a);return this},
enable:function(){return this._setOption("disabled",false)},disable:function(){return this._setOption("disabled",true)},_trigger:function(f,a,c){var h=this.options[f];a=b.Event(a);a.type=(f===this.widgetEventPrefix?f:this.widgetEventPrefix+f).toLowerCase();c=c||{};if(a.originalEvent){f=b.event.props.length;for(var i;f;){i=b.event.props[--f];a[i]=a.originalEvent[i]}}this.element.trigger(a,c);return!(b.isFunction(h)&&h.call(this.element[0],a,c)===false||a.isDefaultPrevented())}}})(jQuery);
(function(b){b.widget("ui.mouse",{options:{cancel:":input,option",distance:1,delay:0},_mouseInit:function(){var d=this;this.element.bind("mousedown."+this.widgetName,function(e){return d._mouseDown(e)}).bind("click."+this.widgetName,function(e){if(true===b.data(e.target,d.widgetName+".preventClickEvent")){b.removeData(e.target,d.widgetName+".preventClickEvent");e.stopImmediatePropagation();return false}});this.started=false},_mouseDestroy:function(){this.element.unbind("."+this.widgetName)},_mouseDown:function(d){d.originalEvent=
d.originalEvent||{};if(!d.originalEvent.mouseHandled){this._mouseStarted&&this._mouseUp(d);this._mouseDownEvent=d;var e=this,g=d.which==1,f=typeof this.options.cancel=="string"?b(d.target).parents().add(d.target).filter(this.options.cancel).length:false;if(!g||f||!this._mouseCapture(d))return true;this.mouseDelayMet=!this.options.delay;if(!this.mouseDelayMet)this._mouseDelayTimer=setTimeout(function(){e.mouseDelayMet=true},this.options.delay);if(this._mouseDistanceMet(d)&&this._mouseDelayMet(d)){this._mouseStarted=
this._mouseStart(d)!==false;if(!this._mouseStarted){d.preventDefault();return true}}true===b.data(d.target,this.widgetName+".preventClickEvent")&&b.removeData(d.target,this.widgetName+".preventClickEvent");this._mouseMoveDelegate=function(a){return e._mouseMove(a)};this._mouseUpDelegate=function(a){return e._mouseUp(a)};b(document).bind("mousemove."+this.widgetName,this._mouseMoveDelegate).bind("mouseup."+this.widgetName,this._mouseUpDelegate);d.preventDefault();return d.originalEvent.mouseHandled=
true}},_mouseMove:function(d){if(b.browser.msie&&!(document.documentMode>=9)&&!d.button)return this._mouseUp(d);if(this._mouseStarted){this._mouseDrag(d);return d.preventDefault()}if(this._mouseDistanceMet(d)&&this._mouseDelayMet(d))(this._mouseStarted=this._mouseStart(this._mouseDownEvent,d)!==false)?this._mouseDrag(d):this._mouseUp(d);return!this._mouseStarted},_mouseUp:function(d){b(document).unbind("mousemove."+this.widgetName,this._mouseMoveDelegate).unbind("mouseup."+this.widgetName,this._mouseUpDelegate);
if(this._mouseStarted){this._mouseStarted=false;d.target==this._mouseDownEvent.target&&b.data(d.target,this.widgetName+".preventClickEvent",true);this._mouseStop(d)}return false},_mouseDistanceMet:function(d){return Math.max(Math.abs(this._mouseDownEvent.pageX-d.pageX),Math.abs(this._mouseDownEvent.pageY-d.pageY))>=this.options.distance},_mouseDelayMet:function(){return this.mouseDelayMet},_mouseStart:function(){},_mouseDrag:function(){},_mouseStop:function(){},_mouseCapture:function(){return true}})})(jQuery);
(function(b){b.widget("ui.draggable",b.ui.mouse,{widgetEventPrefix:"drag",options:{addClasses:true,appendTo:"parent",axis:false,connectToSortable:false,containment:false,cursor:"auto",cursorAt:false,grid:false,handle:false,helper:"original",iframeFix:false,opacity:false,refreshPositions:false,revert:false,revertDuration:500,scope:"default",scroll:true,scrollSensitivity:20,scrollSpeed:20,snap:false,snapMode:"both",snapTolerance:20,stack:false,zIndex:false},_create:function(){if(this.options.helper==
"original"&&!/^(?:r|a|f)/.test(this.element.css("position")))this.element[0].style.position="relative";this.options.addClasses&&this.element.addClass("ui-draggable");this.options.disabled&&this.element.addClass("ui-draggable-disabled");this._mouseInit()},destroy:function(){if(this.element.data("draggable")){this.element.removeData("draggable").unbind(".draggable").removeClass("ui-draggable ui-draggable-dragging ui-draggable-disabled");this._mouseDestroy();return this}},_mouseCapture:function(d){var e=
this.options;if(this.helper||e.disabled||b(d.target).is(".ui-resizable-handle"))return false;this.handle=this._getHandle(d);if(!this.handle)return false;return true},_mouseStart:function(d){var e=this.options;this.helper=this._createHelper(d);this._cacheHelperProportions();if(b.ui.ddmanager)b.ui.ddmanager.current=this;this._cacheMargins();this.cssPosition=this.helper.css("position");this.scrollParent=this.helper.scrollParent();this.offset=this.positionAbs=this.element.offset();this.offset={top:this.offset.top-
this.margins.top,left:this.offset.left-this.margins.left};b.extend(this.offset,{click:{left:d.pageX-this.offset.left,top:d.pageY-this.offset.top},parent:this._getParentOffset(),relative:this._getRelativeOffset()});this.originalPosition=this.position=this._generatePosition(d);this.originalPageX=d.pageX;this.originalPageY=d.pageY;e.cursorAt&&this._adjustOffsetFromHelper(e.cursorAt);e.containment&&this._setContainment();if(this._trigger("start",d)===false){this._clear();return false}this._cacheHelperProportions();
b.ui.ddmanager&&!e.dropBehaviour&&b.ui.ddmanager.prepareOffsets(this,d);this.helper.addClass("ui-draggable-dragging");this._mouseDrag(d,true);return true},_mouseDrag:function(d,e){this.position=this._generatePosition(d);this.positionAbs=this._convertPositionTo("absolute");if(!e){e=this._uiHash();if(this._trigger("drag",d,e)===false){this._mouseUp({});return false}this.position=e.position}if(!this.options.axis||this.options.axis!="y")this.helper[0].style.left=this.position.left+"px";if(!this.options.axis||
this.options.axis!="x")this.helper[0].style.top=this.position.top+"px";b.ui.ddmanager&&b.ui.ddmanager.drag(this,d);return false},_mouseStop:function(d){var e=false;if(b.ui.ddmanager&&!this.options.dropBehaviour)e=b.ui.ddmanager.drop(this,d);if(this.dropped){e=this.dropped;this.dropped=false}if((!this.element[0]||!this.element[0].parentNode)&&this.options.helper=="original")return false;if(this.options.revert=="invalid"&&!e||this.options.revert=="valid"&&e||this.options.revert===true||b.isFunction(this.options.revert)&&
this.options.revert.call(this.element,e)){var g=this;b(this.helper).animate(this.originalPosition,parseInt(this.options.revertDuration,10),function(){g._trigger("stop",d)!==false&&g._clear()})}else this._trigger("stop",d)!==false&&this._clear();return false},cancel:function(){this.helper.is(".ui-draggable-dragging")?this._mouseUp({}):this._clear();return this},_getHandle:function(d){var e=!this.options.handle||!b(this.options.handle,this.element).length?true:false;b(this.options.handle,this.element).find("*").andSelf().each(function(){if(this==
d.target)e=true});return e},_createHelper:function(d){var e=this.options;d=b.isFunction(e.helper)?b(e.helper.apply(this.element[0],[d])):e.helper=="clone"?this.element.clone():this.element;d.parents("body").length||d.appendTo(e.appendTo=="parent"?this.element[0].parentNode:e.appendTo);d[0]!=this.element[0]&&!/(fixed|absolute)/.test(d.css("position"))&&d.css("position","absolute");return d},_adjustOffsetFromHelper:function(d){if(typeof d=="string")d=d.split(" ");if(b.isArray(d))d={left:+d[0],top:+d[1]||
0};if("left"in d)this.offset.click.left=d.left+this.margins.left;if("right"in d)this.offset.click.left=this.helperProportions.width-d.right+this.margins.left;if("top"in d)this.offset.click.top=d.top+this.margins.top;if("bottom"in d)this.offset.click.top=this.helperProportions.height-d.bottom+this.margins.top},_getParentOffset:function(){this.offsetParent=this.helper.offsetParent();var d=this.offsetParent.offset();if(this.cssPosition=="absolute"&&this.scrollParent[0]!=document&&b.ui.contains(this.scrollParent[0],
this.offsetParent[0])){d.left+=this.scrollParent.scrollLeft();d.top+=this.scrollParent.scrollTop()}if(this.offsetParent[0]==document.body||this.offsetParent[0].tagName&&this.offsetParent[0].tagName.toLowerCase()=="html"&&b.browser.msie)d={top:0,left:0};return{top:d.top+(parseInt(this.offsetParent.css("borderTopWidth"),10)||0),left:d.left+(parseInt(this.offsetParent.css("borderLeftWidth"),10)||0)}},_getRelativeOffset:function(){if(this.cssPosition=="relative"){var d=this.element.position();return{top:d.top-
(parseInt(this.helper.css("top"),10)||0)+this.scrollParent.scrollTop(),left:d.left-(parseInt(this.helper.css("left"),10)||0)+this.scrollParent.scrollLeft()}}else return{top:0,left:0}},_cacheMargins:function(){this.margins={left:parseInt(this.element.css("marginLeft"),10)||0,top:parseInt(this.element.css("marginTop"),10)||0,right:parseInt(this.element.css("marginRight"),10)||0,bottom:parseInt(this.element.css("marginBottom"),10)||0}},_cacheHelperProportions:function(){this.helperProportions={width:this.helper.outerWidth(),
height:this.helper.outerHeight()}},_setContainment:function(){var d=this.options;if(d.containment=="parent")d.containment=this.helper[0].parentNode;if(d.containment=="document"||d.containment=="window")this.containment=[(d.containment=="document"?0:b(window).scrollLeft())-this.offset.relative.left-this.offset.parent.left,(d.containment=="document"?0:b(window).scrollTop())-this.offset.relative.top-this.offset.parent.top,(d.containment=="document"?0:b(window).scrollLeft())+b(d.containment=="document"?
document:window).width()-this.helperProportions.width-this.margins.left,(d.containment=="document"?0:b(window).scrollTop())+(b(d.containment=="document"?document:window).height()||document.body.parentNode.scrollHeight)-this.helperProportions.height-this.margins.top];if(!/^(document|window|parent)$/.test(d.containment)&&d.containment.constructor!=Array){var e=b(d.containment)[0];if(e){d=b(d.containment).offset();var g=b(e).css("overflow")!="hidden";this.containment=[d.left+(parseInt(b(e).css("borderLeftWidth"),
10)||0)+(parseInt(b(e).css("paddingLeft"),10)||0),d.top+(parseInt(b(e).css("borderTopWidth"),10)||0)+(parseInt(b(e).css("paddingTop"),10)||0),d.left+(g?Math.max(e.scrollWidth,e.offsetWidth):e.offsetWidth)-(parseInt(b(e).css("borderLeftWidth"),10)||0)-(parseInt(b(e).css("paddingRight"),10)||0)-this.helperProportions.width-this.margins.left-this.margins.right,d.top+(g?Math.max(e.scrollHeight,e.offsetHeight):e.offsetHeight)-(parseInt(b(e).css("borderTopWidth"),10)||0)-(parseInt(b(e).css("paddingBottom"),
10)||0)-this.helperProportions.height-this.margins.top-this.margins.bottom]}}else if(d.containment.constructor==Array)this.containment=d.containment},_convertPositionTo:function(d,e){if(!e)e=this.position;d=d=="absolute"?1:-1;var g=this.cssPosition=="absolute"&&!(this.scrollParent[0]!=document&&b.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,f=/(html|body)/i.test(g[0].tagName);return{top:e.top+this.offset.relative.top*d+this.offset.parent.top*d-(b.browser.safari&&
b.browser.version<526&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollTop():f?0:g.scrollTop())*d),left:e.left+this.offset.relative.left*d+this.offset.parent.left*d-(b.browser.safari&&b.browser.version<526&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():f?0:g.scrollLeft())*d)}},_generatePosition:function(d){var e=this.options,g=this.cssPosition=="absolute"&&!(this.scrollParent[0]!=document&&b.ui.contains(this.scrollParent[0],
this.offsetParent[0]))?this.offsetParent:this.scrollParent,f=/(html|body)/i.test(g[0].tagName),a=d.pageX,c=d.pageY;if(this.originalPosition){if(this.containment){if(d.pageX-this.offset.click.left<this.containment[0])a=this.containment[0]+this.offset.click.left;if(d.pageY-this.offset.click.top<this.containment[1])c=this.containment[1]+this.offset.click.top;if(d.pageX-this.offset.click.left>this.containment[2])a=this.containment[2]+this.offset.click.left;if(d.pageY-this.offset.click.top>this.containment[3])c=
this.containment[3]+this.offset.click.top}if(e.grid){c=this.originalPageY+Math.round((c-this.originalPageY)/e.grid[1])*e.grid[1];c=this.containment?!(c-this.offset.click.top<this.containment[1]||c-this.offset.click.top>this.containment[3])?c:!(c-this.offset.click.top<this.containment[1])?c-e.grid[1]:c+e.grid[1]:c;a=this.originalPageX+Math.round((a-this.originalPageX)/e.grid[0])*e.grid[0];a=this.containment?!(a-this.offset.click.left<this.containment[0]||a-this.offset.click.left>this.containment[2])?
a:!(a-this.offset.click.left<this.containment[0])?a-e.grid[0]:a+e.grid[0]:a}}return{top:c-this.offset.click.top-this.offset.relative.top-this.offset.parent.top+(b.browser.safari&&b.browser.version<526&&this.cssPosition=="fixed"?0:this.cssPosition=="fixed"?-this.scrollParent.scrollTop():f?0:g.scrollTop()),left:a-this.offset.click.left-this.offset.relative.left-this.offset.parent.left+(b.browser.safari&&b.browser.version<526&&this.cssPosition=="fixed"?0:this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():
f?0:g.scrollLeft())}},_clear:function(){this.helper.removeClass("ui-draggable-dragging");this.helper[0]!=this.element[0]&&!this.cancelHelperRemoval&&this.helper.remove();this.helper=null;this.cancelHelperRemoval=false},_trigger:function(d,e,g){g=g||this._uiHash();b.ui.plugin.call(this,d,[e,g]);if(d=="drag")this.positionAbs=this._convertPositionTo("absolute");return b.Widget.prototype._trigger.call(this,d,e,g)},plugins:{},_uiHash:function(){return{helper:this.helper,position:this.position,originalPosition:this.originalPosition,
offset:this.positionAbs}}});b.extend(b.ui.draggable,{version:"1.8.11"});b.ui.plugin.add("draggable","connectToSortable",{start:function(d,e){var g=b(this).data("draggable"),f=g.options,a=b.extend({},e,{item:g.element});g.sortables=[];b(f.connectToSortable).each(function(){var c=b.data(this,"sortable");if(c&&!c.options.disabled){g.sortables.push({instance:c,shouldRevert:c.options.revert});c.refreshPositions();c._trigger("activate",d,a)}})},stop:function(d,e){var g=b(this).data("draggable"),f=b.extend({},
e,{item:g.element});b.each(g.sortables,function(){if(this.instance.isOver){this.instance.isOver=0;g.cancelHelperRemoval=true;this.instance.cancelHelperRemoval=false;if(this.shouldRevert)this.instance.options.revert=true;this.instance._mouseStop(d);this.instance.options.helper=this.instance.options._helper;g.options.helper=="original"&&this.instance.currentItem.css({top:"auto",left:"auto"})}else{this.instance.cancelHelperRemoval=false;this.instance._trigger("deactivate",d,f)}})},drag:function(d,e){var g=
b(this).data("draggable"),f=this;b.each(g.sortables,function(){this.instance.positionAbs=g.positionAbs;this.instance.helperProportions=g.helperProportions;this.instance.offset.click=g.offset.click;if(this.instance._intersectsWith(this.instance.containerCache)){if(!this.instance.isOver){this.instance.isOver=1;this.instance.currentItem=b(f).clone().appendTo(this.instance.element).data("sortable-item",true);this.instance.options._helper=this.instance.options.helper;this.instance.options.helper=function(){return e.helper[0]};
d.target=this.instance.currentItem[0];this.instance._mouseCapture(d,true);this.instance._mouseStart(d,true,true);this.instance.offset.click.top=g.offset.click.top;this.instance.offset.click.left=g.offset.click.left;this.instance.offset.parent.left-=g.offset.parent.left-this.instance.offset.parent.left;this.instance.offset.parent.top-=g.offset.parent.top-this.instance.offset.parent.top;g._trigger("toSortable",d);g.dropped=this.instance.element;g.currentItem=g.element;this.instance.fromOutside=g}this.instance.currentItem&&
this.instance._mouseDrag(d)}else if(this.instance.isOver){this.instance.isOver=0;this.instance.cancelHelperRemoval=true;this.instance.options.revert=false;this.instance._trigger("out",d,this.instance._uiHash(this.instance));this.instance._mouseStop(d,true);this.instance.options.helper=this.instance.options._helper;this.instance.currentItem.remove();this.instance.placeholder&&this.instance.placeholder.remove();g._trigger("fromSortable",d);g.dropped=false}})}});b.ui.plugin.add("draggable","cursor",
{start:function(){var d=b("body"),e=b(this).data("draggable").options;if(d.css("cursor"))e._cursor=d.css("cursor");d.css("cursor",e.cursor)},stop:function(){var d=b(this).data("draggable").options;d._cursor&&b("body").css("cursor",d._cursor)}});b.ui.plugin.add("draggable","iframeFix",{start:function(){var d=b(this).data("draggable").options;b(d.iframeFix===true?"iframe":d.iframeFix).each(function(){b('<div class="ui-draggable-iframeFix" style="background: #fff;"></div>').css({width:this.offsetWidth+
"px",height:this.offsetHeight+"px",position:"absolute",opacity:"0.001",zIndex:1E3}).css(b(this).offset()).appendTo("body")})},stop:function(){b("div.ui-draggable-iframeFix").each(function(){this.parentNode.removeChild(this)})}});b.ui.plugin.add("draggable","opacity",{start:function(d,e){d=b(e.helper);e=b(this).data("draggable").options;if(d.css("opacity"))e._opacity=d.css("opacity");d.css("opacity",e.opacity)},stop:function(d,e){d=b(this).data("draggable").options;d._opacity&&b(e.helper).css("opacity",
d._opacity)}});b.ui.plugin.add("draggable","scroll",{start:function(){var d=b(this).data("draggable");if(d.scrollParent[0]!=document&&d.scrollParent[0].tagName!="HTML")d.overflowOffset=d.scrollParent.offset()},drag:function(d){var e=b(this).data("draggable"),g=e.options,f=false;if(e.scrollParent[0]!=document&&e.scrollParent[0].tagName!="HTML"){if(!g.axis||g.axis!="x")if(e.overflowOffset.top+e.scrollParent[0].offsetHeight-d.pageY<g.scrollSensitivity)e.scrollParent[0].scrollTop=f=e.scrollParent[0].scrollTop+
g.scrollSpeed;else if(d.pageY-e.overflowOffset.top<g.scrollSensitivity)e.scrollParent[0].scrollTop=f=e.scrollParent[0].scrollTop-g.scrollSpeed;if(!g.axis||g.axis!="y")if(e.overflowOffset.left+e.scrollParent[0].offsetWidth-d.pageX<g.scrollSensitivity)e.scrollParent[0].scrollLeft=f=e.scrollParent[0].scrollLeft+g.scrollSpeed;else if(d.pageX-e.overflowOffset.left<g.scrollSensitivity)e.scrollParent[0].scrollLeft=f=e.scrollParent[0].scrollLeft-g.scrollSpeed}else{if(!g.axis||g.axis!="x")if(d.pageY-b(document).scrollTop()<
g.scrollSensitivity)f=b(document).scrollTop(b(document).scrollTop()-g.scrollSpeed);else if(b(window).height()-(d.pageY-b(document).scrollTop())<g.scrollSensitivity)f=b(document).scrollTop(b(document).scrollTop()+g.scrollSpeed);if(!g.axis||g.axis!="y")if(d.pageX-b(document).scrollLeft()<g.scrollSensitivity)f=b(document).scrollLeft(b(document).scrollLeft()-g.scrollSpeed);else if(b(window).width()-(d.pageX-b(document).scrollLeft())<g.scrollSensitivity)f=b(document).scrollLeft(b(document).scrollLeft()+
g.scrollSpeed)}f!==false&&b.ui.ddmanager&&!g.dropBehaviour&&b.ui.ddmanager.prepareOffsets(e,d)}});b.ui.plugin.add("draggable","snap",{start:function(){var d=b(this).data("draggable"),e=d.options;d.snapElements=[];b(e.snap.constructor!=String?e.snap.items||":data(draggable)":e.snap).each(function(){var g=b(this),f=g.offset();this!=d.element[0]&&d.snapElements.push({item:this,width:g.outerWidth(),height:g.outerHeight(),top:f.top,left:f.left})})},drag:function(d,e){for(var g=b(this).data("draggable"),
f=g.options,a=f.snapTolerance,c=e.offset.left,h=c+g.helperProportions.width,i=e.offset.top,j=i+g.helperProportions.height,n=g.snapElements.length-1;n>=0;n--){var p=g.snapElements[n].left,l=p+g.snapElements[n].width,k=g.snapElements[n].top,m=k+g.snapElements[n].height;if(p-a<c&&c<l+a&&k-a<i&&i<m+a||p-a<c&&c<l+a&&k-a<j&&j<m+a||p-a<h&&h<l+a&&k-a<i&&i<m+a||p-a<h&&h<l+a&&k-a<j&&j<m+a){if(f.snapMode!="inner"){var o=Math.abs(k-j)<=a,q=Math.abs(m-i)<=a,s=Math.abs(p-h)<=a,r=Math.abs(l-c)<=a;if(o)e.position.top=
g._convertPositionTo("relative",{top:k-g.helperProportions.height,left:0}).top-g.margins.top;if(q)e.position.top=g._convertPositionTo("relative",{top:m,left:0}).top-g.margins.top;if(s)e.position.left=g._convertPositionTo("relative",{top:0,left:p-g.helperProportions.width}).left-g.margins.left;if(r)e.position.left=g._convertPositionTo("relative",{top:0,left:l}).left-g.margins.left}var u=o||q||s||r;if(f.snapMode!="outer"){o=Math.abs(k-i)<=a;q=Math.abs(m-j)<=a;s=Math.abs(p-c)<=a;r=Math.abs(l-h)<=a;if(o)e.position.top=
g._convertPositionTo("relative",{top:k,left:0}).top-g.margins.top;if(q)e.position.top=g._convertPositionTo("relative",{top:m-g.helperProportions.height,left:0}).top-g.margins.top;if(s)e.position.left=g._convertPositionTo("relative",{top:0,left:p}).left-g.margins.left;if(r)e.position.left=g._convertPositionTo("relative",{top:0,left:l-g.helperProportions.width}).left-g.margins.left}if(!g.snapElements[n].snapping&&(o||q||s||r||u))g.options.snap.snap&&g.options.snap.snap.call(g.element,d,b.extend(g._uiHash(),
{snapItem:g.snapElements[n].item}));g.snapElements[n].snapping=o||q||s||r||u}else{g.snapElements[n].snapping&&g.options.snap.release&&g.options.snap.release.call(g.element,d,b.extend(g._uiHash(),{snapItem:g.snapElements[n].item}));g.snapElements[n].snapping=false}}}});b.ui.plugin.add("draggable","stack",{start:function(){var d=b(this).data("draggable").options;d=b.makeArray(b(d.stack)).sort(function(g,f){return(parseInt(b(g).css("zIndex"),10)||0)-(parseInt(b(f).css("zIndex"),10)||0)});if(d.length){var e=
parseInt(d[0].style.zIndex)||0;b(d).each(function(g){this.style.zIndex=e+g});this[0].style.zIndex=e+d.length}}});b.ui.plugin.add("draggable","zIndex",{start:function(d,e){d=b(e.helper);e=b(this).data("draggable").options;if(d.css("zIndex"))e._zIndex=d.css("zIndex");d.css("zIndex",e.zIndex)},stop:function(d,e){d=b(this).data("draggable").options;d._zIndex&&b(e.helper).css("zIndex",d._zIndex)}})})(jQuery);
(function(b){b.widget("ui.droppable",{widgetEventPrefix:"drop",options:{accept:"*",activeClass:false,addClasses:true,greedy:false,hoverClass:false,scope:"default",tolerance:"intersect"},_create:function(){var d=this.options,e=d.accept;this.isover=0;this.isout=1;this.accept=b.isFunction(e)?e:function(g){return g.is(e)};this.proportions={width:this.element[0].offsetWidth,height:this.element[0].offsetHeight};b.ui.ddmanager.droppables[d.scope]=b.ui.ddmanager.droppables[d.scope]||[];b.ui.ddmanager.droppables[d.scope].push(this);
d.addClasses&&this.element.addClass("ui-droppable")},destroy:function(){for(var d=b.ui.ddmanager.droppables[this.options.scope],e=0;e<d.length;e++)d[e]==this&&d.splice(e,1);this.element.removeClass("ui-droppable ui-droppable-disabled").removeData("droppable").unbind(".droppable");return this},_setOption:function(d,e){if(d=="accept")this.accept=b.isFunction(e)?e:function(g){return g.is(e)};b.Widget.prototype._setOption.apply(this,arguments)},_activate:function(d){var e=b.ui.ddmanager.current;this.options.activeClass&&
this.element.addClass(this.options.activeClass);e&&this._trigger("activate",d,this.ui(e))},_deactivate:function(d){var e=b.ui.ddmanager.current;this.options.activeClass&&this.element.removeClass(this.options.activeClass);e&&this._trigger("deactivate",d,this.ui(e))},_over:function(d){var e=b.ui.ddmanager.current;if(!(!e||(e.currentItem||e.element)[0]==this.element[0]))if(this.accept.call(this.element[0],e.currentItem||e.element)){this.options.hoverClass&&this.element.addClass(this.options.hoverClass);
this._trigger("over",d,this.ui(e))}},_out:function(d){var e=b.ui.ddmanager.current;if(!(!e||(e.currentItem||e.element)[0]==this.element[0]))if(this.accept.call(this.element[0],e.currentItem||e.element)){this.options.hoverClass&&this.element.removeClass(this.options.hoverClass);this._trigger("out",d,this.ui(e))}},_drop:function(d,e){var g=e||b.ui.ddmanager.current;if(!g||(g.currentItem||g.element)[0]==this.element[0])return false;var f=false;this.element.find(":data(droppable)").not(".ui-draggable-dragging").each(function(){var a=
b.data(this,"droppable");if(a.options.greedy&&!a.options.disabled&&a.options.scope==g.options.scope&&a.accept.call(a.element[0],g.currentItem||g.element)&&b.ui.intersect(g,b.extend(a,{offset:a.element.offset()}),a.options.tolerance)){f=true;return false}});if(f)return false;if(this.accept.call(this.element[0],g.currentItem||g.element)){this.options.activeClass&&this.element.removeClass(this.options.activeClass);this.options.hoverClass&&this.element.removeClass(this.options.hoverClass);this._trigger("drop",
d,this.ui(g));return this.element}return false},ui:function(d){return{draggable:d.currentItem||d.element,helper:d.helper,position:d.position,offset:d.positionAbs}}});b.extend(b.ui.droppable,{version:"1.8.11"});b.ui.intersect=function(d,e,g){if(!e.offset)return false;var f=(d.positionAbs||d.position.absolute).left,a=f+d.helperProportions.width,c=(d.positionAbs||d.position.absolute).top,h=c+d.helperProportions.height,i=e.offset.left,j=i+e.proportions.width,n=e.offset.top,p=n+e.proportions.height;
switch(g){case "fit":return i<=f&&a<=j&&n<=c&&h<=p;case "intersect":return i<f+d.helperProportions.width/2&&a-d.helperProportions.width/2<j&&n<c+d.helperProportions.height/2&&h-d.helperProportions.height/2<p;case "pointer":return b.ui.isOver((d.positionAbs||d.position.absolute).top+(d.clickOffset||d.offset.click).top,(d.positionAbs||d.position.absolute).left+(d.clickOffset||d.offset.click).left,n,i,e.proportions.height,e.proportions.width);case "touch":return(c>=n&&c<=p||h>=n&&h<=p||c<n&&h>p)&&(f>=
i&&f<=j||a>=i&&a<=j||f<i&&a>j);default:return false}};b.ui.ddmanager={current:null,droppables:{"default":[]},prepareOffsets:function(d,e){var g=b.ui.ddmanager.droppables[d.options.scope]||[],f=e?e.type:null,a=(d.currentItem||d.element).find(":data(droppable)").andSelf(),c=0;a:for(;c<g.length;c++)if(!(g[c].options.disabled||d&&!g[c].accept.call(g[c].element[0],d.currentItem||d.element))){for(var h=0;h<a.length;h++)if(a[h]==g[c].element[0]){g[c].proportions.height=0;continue a}g[c].visible=g[c].element.css("display")!=
"none";if(g[c].visible){f=="mousedown"&&g[c]._activate.call(g[c],e);g[c].offset=g[c].element.offset();g[c].proportions={width:g[c].element[0].offsetWidth,height:g[c].element[0].offsetHeight}}}},drop:function(d,e){var g=false;b.each(b.ui.ddmanager.droppables[d.options.scope]||[],function(){if(this.options){if(!this.options.disabled&&this.visible&&b.ui.intersect(d,this,this.options.tolerance))g=g||this._drop.call(this,e);if(!this.options.disabled&&this.visible&&this.accept.call(this.element[0],d.currentItem||
d.element)){this.isout=1;this.isover=0;this._deactivate.call(this,e)}}});return g},drag:function(d,e){d.options.refreshPositions&&b.ui.ddmanager.prepareOffsets(d,e);b.each(b.ui.ddmanager.droppables[d.options.scope]||[],function(){if(!(this.options.disabled||this.greedyChild||!this.visible)){var g=b.ui.intersect(d,this,this.options.tolerance);if(g=!g&&this.isover==1?"isout":g&&this.isover==0?"isover":null){var f;if(this.options.greedy){var a=this.element.parents(":data(droppable):eq(0)");if(a.length){f=
b.data(a[0],"droppable");f.greedyChild=g=="isover"?1:0}}if(f&&g=="isover"){f.isover=0;f.isout=1;f._out.call(f,e)}this[g]=1;this[g=="isout"?"isover":"isout"]=0;this[g=="isover"?"_over":"_out"].call(this,e);if(f&&g=="isout"){f.isout=0;f.isover=1;f._over.call(f,e)}}}})}}})(jQuery);
(function(b){b.widget("ui.resizable",b.ui.mouse,{widgetEventPrefix:"resize",options:{alsoResize:false,animate:false,animateDuration:"slow",animateEasing:"swing",aspectRatio:false,autoHide:false,containment:false,ghost:false,grid:false,handles:"e,s,se",helper:false,maxHeight:null,maxWidth:null,minHeight:10,minWidth:10,zIndex:1E3},_create:function(){var g=this,f=this.options;this.element.addClass("ui-resizable");b.extend(this,{_aspectRatio:!!f.aspectRatio,aspectRatio:f.aspectRatio,originalElement:this.element,
_proportionallyResizeElements:[],_helper:f.helper||f.ghost||f.animate?f.helper||"ui-resizable-helper":null});if(this.element[0].nodeName.match(/canvas|textarea|input|select|button|img/i)){/relative/.test(this.element.css("position"))&&b.browser.opera&&this.element.css({position:"relative",top:"auto",left:"auto"});this.element.wrap(b('<div class="ui-wrapper" style="overflow: hidden;"></div>').css({position:this.element.css("position"),width:this.element.outerWidth(),height:this.element.outerHeight(),
top:this.element.css("top"),left:this.element.css("left")}));this.element=this.element.parent().data("resizable",this.element.data("resizable"));this.elementIsWrapper=true;this.element.css({marginLeft:this.originalElement.css("marginLeft"),marginTop:this.originalElement.css("marginTop"),marginRight:this.originalElement.css("marginRight"),marginBottom:this.originalElement.css("marginBottom")});this.originalElement.css({marginLeft:0,marginTop:0,marginRight:0,marginBottom:0});this.originalResizeStyle=
this.originalElement.css("resize");this.originalElement.css("resize","none");this._proportionallyResizeElements.push(this.originalElement.css({position:"static",zoom:1,display:"block"}));this.originalElement.css({margin:this.originalElement.css("margin")});this._proportionallyResize()}this.handles=f.handles||(!b(".ui-resizable-handle",this.element).length?"e,s,se":{n:".ui-resizable-n",e:".ui-resizable-e",s:".ui-resizable-s",w:".ui-resizable-w",se:".ui-resizable-se",sw:".ui-resizable-sw",ne:".ui-resizable-ne",
nw:".ui-resizable-nw"});if(this.handles.constructor==String){if(this.handles=="all")this.handles="n,e,s,w,se,sw,ne,nw";var a=this.handles.split(",");this.handles={};for(var c=0;c<a.length;c++){var h=b.trim(a[c]),i=b('<div class="ui-resizable-handle '+("ui-resizable-"+h)+'"></div>');/sw|se|ne|nw/.test(h)&&i.css({zIndex:++f.zIndex});"se"==h&&i.addClass("ui-icon ui-icon-gripsmall-diagonal-se");this.handles[h]=".ui-resizable-"+h;this.element.append(i)}}this._renderAxis=function(j){j=j||this.element;for(var n in this.handles){if(this.handles[n].constructor==
String)this.handles[n]=b(this.handles[n],this.element).show();if(this.elementIsWrapper&&this.originalElement[0].nodeName.match(/textarea|input|select|button/i)){var p=b(this.handles[n],this.element),l=0;l=/sw|ne|nw|se|n|s/.test(n)?p.outerHeight():p.outerWidth();p=["padding",/ne|nw|n/.test(n)?"Top":/se|sw|s/.test(n)?"Bottom":/^e$/.test(n)?"Right":"Left"].join("");j.css(p,l);this._proportionallyResize()}b(this.handles[n])}};this._renderAxis(this.element);this._handles=b(".ui-resizable-handle",this.element).disableSelection();
this._handles.mouseover(function(){if(!g.resizing){if(this.className)var j=this.className.match(/ui-resizable-(se|sw|ne|nw|n|e|s|w)/i);g.axis=j&&j[1]?j[1]:"se"}});if(f.autoHide){this._handles.hide();b(this.element).addClass("ui-resizable-autohide").hover(function(){b(this).removeClass("ui-resizable-autohide");g._handles.show()},function(){if(!g.resizing){b(this).addClass("ui-resizable-autohide");g._handles.hide()}})}this._mouseInit()},destroy:function(){this._mouseDestroy();var g=function(a){b(a).removeClass("ui-resizable ui-resizable-disabled ui-resizable-resizing").removeData("resizable").unbind(".resizable").find(".ui-resizable-handle").remove()};
if(this.elementIsWrapper){g(this.element);var f=this.element;f.after(this.originalElement.css({position:f.css("position"),width:f.outerWidth(),height:f.outerHeight(),top:f.css("top"),left:f.css("left")})).remove()}this.originalElement.css("resize",this.originalResizeStyle);g(this.originalElement);return this},_mouseCapture:function(g){var f=false;for(var a in this.handles)if(b(this.handles[a])[0]==g.target)f=true;return!this.options.disabled&&f},_mouseStart:function(g){var f=this.options,a=this.element.position(),
c=this.element;this.resizing=true;this.documentScroll={top:b(document).scrollTop(),left:b(document).scrollLeft()};if(c.is(".ui-draggable")||/absolute/.test(c.css("position")))c.css({position:"absolute",top:a.top,left:a.left});b.browser.opera&&/relative/.test(c.css("position"))&&c.css({position:"relative",top:"auto",left:"auto"});this._renderProxy();a=d(this.helper.css("left"));var h=d(this.helper.css("top"));if(f.containment){a+=b(f.containment).scrollLeft()||0;h+=b(f.containment).scrollTop()||0}this.offset=
this.helper.offset();this.position={left:a,top:h};this.size=this._helper?{width:c.outerWidth(),height:c.outerHeight()}:{width:c.width(),height:c.height()};this.originalSize=this._helper?{width:c.outerWidth(),height:c.outerHeight()}:{width:c.width(),height:c.height()};this.originalPosition={left:a,top:h};this.sizeDiff={width:c.outerWidth()-c.width(),height:c.outerHeight()-c.height()};this.originalMousePosition={left:g.pageX,top:g.pageY};this.aspectRatio=typeof f.aspectRatio=="number"?f.aspectRatio:
this.originalSize.width/this.originalSize.height||1;f=b(".ui-resizable-"+this.axis).css("cursor");b("body").css("cursor",f=="auto"?this.axis+"-resize":f);c.addClass("ui-resizable-resizing");this._propagate("start",g);return true},_mouseDrag:function(g){var f=this.helper,a=this.originalMousePosition,c=this._change[this.axis];if(!c)return false;a=c.apply(this,[g,g.pageX-a.left||0,g.pageY-a.top||0]);if(this._aspectRatio||g.shiftKey)a=this._updateRatio(a,g);a=this._respectSize(a,g);this._propagate("resize",
g);f.css({top:this.position.top+"px",left:this.position.left+"px",width:this.size.width+"px",height:this.size.height+"px"});!this._helper&&this._proportionallyResizeElements.length&&this._proportionallyResize();this._updateCache(a);this._trigger("resize",g,this.ui());return false},_mouseStop:function(g){this.resizing=false;var f=this.options,a=this;if(this._helper){var c=this._proportionallyResizeElements,h=c.length&&/textarea/i.test(c[0].nodeName);c=h&&b.ui.hasScroll(c[0],"left")?0:a.sizeDiff.height;
h=h?0:a.sizeDiff.width;h={width:a.helper.width()-h,height:a.helper.height()-c};c=parseInt(a.element.css("left"),10)+(a.position.left-a.originalPosition.left)||null;var i=parseInt(a.element.css("top"),10)+(a.position.top-a.originalPosition.top)||null;f.animate||this.element.css(b.extend(h,{top:i,left:c}));a.helper.height(a.size.height);a.helper.width(a.size.width);this._helper&&!f.animate&&this._proportionallyResize()}b("body").css("cursor","auto");this.element.removeClass("ui-resizable-resizing");
this._propagate("stop",g);this._helper&&this.helper.remove();return false},_updateCache:function(g){this.offset=this.helper.offset();if(e(g.left))this.position.left=g.left;if(e(g.top))this.position.top=g.top;if(e(g.height))this.size.height=g.height;if(e(g.width))this.size.width=g.width},_updateRatio:function(g){var f=this.position,a=this.size,c=this.axis;if(g.height)g.width=a.height*this.aspectRatio;else if(g.width)g.height=a.width/this.aspectRatio;if(c=="sw"){g.left=f.left+(a.width-g.width);g.top=
null}if(c=="nw"){g.top=f.top+(a.height-g.height);g.left=f.left+(a.width-g.width)}return g},_respectSize:function(g){var f=this.options,a=this.axis,c=e(g.width)&&f.maxWidth&&f.maxWidth<g.width,h=e(g.height)&&f.maxHeight&&f.maxHeight<g.height,i=e(g.width)&&f.minWidth&&f.minWidth>g.width,j=e(g.height)&&f.minHeight&&f.minHeight>g.height;if(i)g.width=f.minWidth;if(j)g.height=f.minHeight;if(c)g.width=f.maxWidth;if(h)g.height=f.maxHeight;var n=this.originalPosition.left+this.originalSize.width,p=this.position.top+
this.size.height,l=/sw|nw|w/.test(a);a=/nw|ne|n/.test(a);if(i&&l)g.left=n-f.minWidth;if(c&&l)g.left=n-f.maxWidth;if(j&&a)g.top=p-f.minHeight;if(h&&a)g.top=p-f.maxHeight;if((f=!g.width&&!g.height)&&!g.left&&g.top)g.top=null;else if(f&&!g.top&&g.left)g.left=null;return g},_proportionallyResize:function(){if(this._proportionallyResizeElements.length)for(var g=this.helper||this.element,f=0;f<this._proportionallyResizeElements.length;f++){var a=this._proportionallyResizeElements[f];if(!this.borderDif){var c=
[a.css("borderTopWidth"),a.css("borderRightWidth"),a.css("borderBottomWidth"),a.css("borderLeftWidth")],h=[a.css("paddingTop"),a.css("paddingRight"),a.css("paddingBottom"),a.css("paddingLeft")];this.borderDif=b.map(c,function(i,j){i=parseInt(i,10)||0;j=parseInt(h[j],10)||0;return i+j})}b.browser.msie&&(b(g).is(":hidden")||b(g).parents(":hidden").length)||a.css({height:g.height()-this.borderDif[0]-this.borderDif[2]||0,width:g.width()-this.borderDif[1]-this.borderDif[3]||0})}},_renderProxy:function(){var g=
this.options;this.elementOffset=this.element.offset();if(this._helper){this.helper=this.helper||b('<div style="overflow:hidden;"></div>');var f=b.browser.msie&&b.browser.version<7,a=f?1:0;f=f?2:-1;this.helper.addClass(this._helper).css({width:this.element.outerWidth()+f,height:this.element.outerHeight()+f,position:"absolute",left:this.elementOffset.left-a+"px",top:this.elementOffset.top-a+"px",zIndex:++g.zIndex});this.helper.appendTo("body").disableSelection()}else this.helper=this.element},_change:{e:function(g,
f){return{width:this.originalSize.width+f}},w:function(g,f){return{left:this.originalPosition.left+f,width:this.originalSize.width-f}},n:function(g,f,a){return{top:this.originalPosition.top+a,height:this.originalSize.height-a}},s:function(g,f,a){return{height:this.originalSize.height+a}},se:function(g,f,a){return b.extend(this._change.s.apply(this,arguments),this._change.e.apply(this,[g,f,a]))},sw:function(g,f,a){return b.extend(this._change.s.apply(this,arguments),this._change.w.apply(this,[g,f,
a]))},ne:function(g,f,a){return b.extend(this._change.n.apply(this,arguments),this._change.e.apply(this,[g,f,a]))},nw:function(g,f,a){return b.extend(this._change.n.apply(this,arguments),this._change.w.apply(this,[g,f,a]))}},_propagate:function(g,f){b.ui.plugin.call(this,g,[f,this.ui()]);g!="resize"&&this._trigger(g,f,this.ui())},plugins:{},ui:function(){return{originalElement:this.originalElement,element:this.element,helper:this.helper,position:this.position,size:this.size,originalSize:this.originalSize,
originalPosition:this.originalPosition}}});b.extend(b.ui.resizable,{version:"1.8.11"});b.ui.plugin.add("resizable","alsoResize",{start:function(){var g=b(this).data("resizable").options,f=function(a){b(a).each(function(){var c=b(this);c.data("resizable-alsoresize",{width:parseInt(c.width(),10),height:parseInt(c.height(),10),left:parseInt(c.css("left"),10),top:parseInt(c.css("top"),10),position:c.css("position")})})};if(typeof g.alsoResize=="object"&&!g.alsoResize.parentNode)if(g.alsoResize.length){g.alsoResize=
g.alsoResize[0];f(g.alsoResize)}else b.each(g.alsoResize,function(a){f(a)});else f(g.alsoResize)},resize:function(g,f){var a=b(this).data("resizable");g=a.options;var c=a.originalSize,h=a.originalPosition,i={height:a.size.height-c.height||0,width:a.size.width-c.width||0,top:a.position.top-h.top||0,left:a.position.left-h.left||0},j=function(n,p){b(n).each(function(){var l=b(this),k=b(this).data("resizable-alsoresize"),m={},o=p&&p.length?p:l.parents(f.originalElement[0]).length?["width","height"]:["width",
"height","top","left"];b.each(o,function(q,s){if((q=(k[s]||0)+(i[s]||0))&&q>=0)m[s]=q||null});if(b.browser.opera&&/relative/.test(l.css("position"))){a._revertToRelativePosition=true;l.css({position:"absolute",top:"auto",left:"auto"})}l.css(m)})};typeof g.alsoResize=="object"&&!g.alsoResize.nodeType?b.each(g.alsoResize,function(n,p){j(n,p)}):j(g.alsoResize)},stop:function(){var g=b(this).data("resizable"),f=g.options,a=function(c){b(c).each(function(){var h=b(this);h.css({position:h.data("resizable-alsoresize").position})})};
if(g._revertToRelativePosition){g._revertToRelativePosition=false;typeof f.alsoResize=="object"&&!f.alsoResize.nodeType?b.each(f.alsoResize,function(c){a(c)}):a(f.alsoResize)}b(this).removeData("resizable-alsoresize")}});b.ui.plugin.add("resizable","animate",{stop:function(g){var f=b(this).data("resizable"),a=f.options,c=f._proportionallyResizeElements,h=c.length&&/textarea/i.test(c[0].nodeName),i=h&&b.ui.hasScroll(c[0],"left")?0:f.sizeDiff.height;h={width:f.size.width-(h?0:f.sizeDiff.width),height:f.size.height-
i};i=parseInt(f.element.css("left"),10)+(f.position.left-f.originalPosition.left)||null;var j=parseInt(f.element.css("top"),10)+(f.position.top-f.originalPosition.top)||null;f.element.animate(b.extend(h,j&&i?{top:j,left:i}:{}),{duration:a.animateDuration,easing:a.animateEasing,step:function(){var n={width:parseInt(f.element.css("width"),10),height:parseInt(f.element.css("height"),10),top:parseInt(f.element.css("top"),10),left:parseInt(f.element.css("left"),10)};c&&c.length&&b(c[0]).css({width:n.width,
height:n.height});f._updateCache(n);f._propagate("resize",g)}})}});b.ui.plugin.add("resizable","containment",{start:function(){var g=b(this).data("resizable"),f=g.element,a=g.options.containment;if(f=a instanceof b?a.get(0):/parent/.test(a)?f.parent().get(0):a){g.containerElement=b(f);if(/document/.test(a)||a==document){g.containerOffset={left:0,top:0};g.containerPosition={left:0,top:0};g.parentData={element:b(document),left:0,top:0,width:b(document).width(),height:b(document).height()||document.body.parentNode.scrollHeight}}else{var c=
b(f),h=[];b(["Top","Right","Left","Bottom"]).each(function(n,p){h[n]=d(c.css("padding"+p))});g.containerOffset=c.offset();g.containerPosition=c.position();g.containerSize={height:c.innerHeight()-h[3],width:c.innerWidth()-h[1]};a=g.containerOffset;var i=g.containerSize.height,j=g.containerSize.width;j=b.ui.hasScroll(f,"left")?f.scrollWidth:j;i=b.ui.hasScroll(f)?f.scrollHeight:i;g.parentData={element:f,left:a.left,top:a.top,width:j,height:i}}}},resize:function(g){var f=b(this).data("resizable"),a=f.options,
c=f.containerOffset,h=f.position;g=f._aspectRatio||g.shiftKey;var i={top:0,left:0},j=f.containerElement;if(j[0]!=document&&/static/.test(j.css("position")))i=c;if(h.left<(f._helper?c.left:0)){f.size.width+=f._helper?f.position.left-c.left:f.position.left-i.left;if(g)f.size.height=f.size.width/a.aspectRatio;f.position.left=a.helper?c.left:0}if(h.top<(f._helper?c.top:0)){f.size.height+=f._helper?f.position.top-c.top:f.position.top;if(g)f.size.width=f.size.height*a.aspectRatio;f.position.top=f._helper?
c.top:0}f.offset.left=f.parentData.left+f.position.left;f.offset.top=f.parentData.top+f.position.top;a=Math.abs((f._helper?f.offset.left-i.left:f.offset.left-i.left)+f.sizeDiff.width);c=Math.abs((f._helper?f.offset.top-i.top:f.offset.top-c.top)+f.sizeDiff.height);h=f.containerElement.get(0)==f.element.parent().get(0);i=/relative|absolute/.test(f.containerElement.css("position"));if(h&&i)a-=f.parentData.left;if(a+f.size.width>=f.parentData.width){f.size.width=f.parentData.width-a;if(g)f.size.height=
f.size.width/f.aspectRatio}if(c+f.size.height>=f.parentData.height){f.size.height=f.parentData.height-c;if(g)f.size.width=f.size.height*f.aspectRatio}},stop:function(){var g=b(this).data("resizable"),f=g.options,a=g.containerOffset,c=g.containerPosition,h=g.containerElement,i=b(g.helper),j=i.offset(),n=i.outerWidth()-g.sizeDiff.width;i=i.outerHeight()-g.sizeDiff.height;g._helper&&!f.animate&&/relative/.test(h.css("position"))&&b(this).css({left:j.left-c.left-a.left,width:n,height:i});g._helper&&!f.animate&&
/static/.test(h.css("position"))&&b(this).css({left:j.left-c.left-a.left,width:n,height:i})}});b.ui.plugin.add("resizable","ghost",{start:function(){var g=b(this).data("resizable"),f=g.options,a=g.size;g.ghost=g.originalElement.clone();g.ghost.css({opacity:0.25,display:"block",position:"relative",height:a.height,width:a.width,margin:0,left:0,top:0}).addClass("ui-resizable-ghost").addClass(typeof f.ghost=="string"?f.ghost:"");g.ghost.appendTo(g.helper)},resize:function(){var g=b(this).data("resizable");
g.ghost&&g.ghost.css({position:"relative",height:g.size.height,width:g.size.width})},stop:function(){var g=b(this).data("resizable");g.ghost&&g.helper&&g.helper.get(0).removeChild(g.ghost.get(0))}});b.ui.plugin.add("resizable","grid",{resize:function(){var g=b(this).data("resizable"),f=g.options,a=g.size,c=g.originalSize,h=g.originalPosition,i=g.axis;f.grid=typeof f.grid=="number"?[f.grid,f.grid]:f.grid;var j=Math.round((a.width-c.width)/(f.grid[0]||1))*(f.grid[0]||1);f=Math.round((a.height-c.height)/
(f.grid[1]||1))*(f.grid[1]||1);if(/^(se|s|e)$/.test(i)){g.size.width=c.width+j;g.size.height=c.height+f}else if(/^(ne)$/.test(i)){g.size.width=c.width+j;g.size.height=c.height+f;g.position.top=h.top-f}else{if(/^(sw)$/.test(i)){g.size.width=c.width+j;g.size.height=c.height+f}else{g.size.width=c.width+j;g.size.height=c.height+f;g.position.top=h.top-f}g.position.left=h.left-j}}});var d=function(g){return parseInt(g,10)||0},e=function(g){return!isNaN(parseInt(g,10))}})(jQuery);
(function(b){b.widget("ui.selectable",b.ui.mouse,{options:{appendTo:"body",autoRefresh:true,distance:0,filter:"*",tolerance:"touch"},_create:function(){var d=this;this.element.addClass("ui-selectable");this.dragged=false;var e;this.refresh=function(){e=b(d.options.filter,d.element[0]);e.each(function(){var g=b(this),f=g.offset();b.data(this,"selectable-item",{element:this,$element:g,left:f.left,top:f.top,right:f.left+g.outerWidth(),bottom:f.top+g.outerHeight(),startselected:false,selected:g.hasClass("ui-selected"),
selecting:g.hasClass("ui-selecting"),unselecting:g.hasClass("ui-unselecting")})})};this.refresh();this.selectees=e.addClass("ui-selectee");this._mouseInit();this.helper=b("<div class='ui-selectable-helper'></div>")},destroy:function(){this.selectees.removeClass("ui-selectee").removeData("selectable-item");this.element.removeClass("ui-selectable ui-selectable-disabled").removeData("selectable").unbind(".selectable");this._mouseDestroy();return this},_mouseStart:function(d){var e=this;this.opos=[d.pageX,
d.pageY];if(!this.options.disabled){var g=this.options;this.selectees=b(g.filter,this.element[0]);this._trigger("start",d);b(g.appendTo).append(this.helper);this.helper.css({left:d.clientX,top:d.clientY,width:0,height:0});g.autoRefresh&&this.refresh();this.selectees.filter(".ui-selected").each(function(){var f=b.data(this,"selectable-item");f.startselected=true;if(!d.metaKey){f.$element.removeClass("ui-selected");f.selected=false;f.$element.addClass("ui-unselecting");f.unselecting=true;e._trigger("unselecting",
d,{unselecting:f.element})}});b(d.target).parents().andSelf().each(function(){var f=b.data(this,"selectable-item");if(f){var a=!d.metaKey||!f.$element.hasClass("ui-selected");f.$element.removeClass(a?"ui-unselecting":"ui-selected").addClass(a?"ui-selecting":"ui-unselecting");f.unselecting=!a;f.selecting=a;(f.selected=a)?e._trigger("selecting",d,{selecting:f.element}):e._trigger("unselecting",d,{unselecting:f.element});return false}})}},_mouseDrag:function(d){var e=this;this.dragged=true;if(!this.options.disabled){var g=
this.options,f=this.opos[0],a=this.opos[1],c=d.pageX,h=d.pageY;if(f>c){var i=c;c=f;f=i}if(a>h){i=h;h=a;a=i}this.helper.css({left:f,top:a,width:c-f,height:h-a});this.selectees.each(function(){var j=b.data(this,"selectable-item");if(!(!j||j.element==e.element[0])){var n=false;if(g.tolerance=="touch")n=!(j.left>c||j.right<f||j.top>h||j.bottom<a);else if(g.tolerance=="fit")n=j.left>f&&j.right<c&&j.top>a&&j.bottom<h;if(n){if(j.selected){j.$element.removeClass("ui-selected");j.selected=false}if(j.unselecting){j.$element.removeClass("ui-unselecting");
j.unselecting=false}if(!j.selecting){j.$element.addClass("ui-selecting");j.selecting=true;e._trigger("selecting",d,{selecting:j.element})}}else{if(j.selecting)if(d.metaKey&&j.startselected){j.$element.removeClass("ui-selecting");j.selecting=false;j.$element.addClass("ui-selected");j.selected=true}else{j.$element.removeClass("ui-selecting");j.selecting=false;if(j.startselected){j.$element.addClass("ui-unselecting");j.unselecting=true}e._trigger("unselecting",d,{unselecting:j.element})}if(j.selected)if(!d.metaKey&&
!j.startselected){j.$element.removeClass("ui-selected");j.selected=false;j.$element.addClass("ui-unselecting");j.unselecting=true;e._trigger("unselecting",d,{unselecting:j.element})}}}});return false}},_mouseStop:function(d){var e=this;this.dragged=false;b(".ui-unselecting",this.element[0]).each(function(){var g=b.data(this,"selectable-item");g.$element.removeClass("ui-unselecting");g.unselecting=false;g.startselected=false;e._trigger("unselected",d,{unselected:g.element})});b(".ui-selecting",this.element[0]).each(function(){var g=
b.data(this,"selectable-item");g.$element.removeClass("ui-selecting").addClass("ui-selected");g.selecting=false;g.selected=true;g.startselected=true;e._trigger("selected",d,{selected:g.element})});this._trigger("stop",d);this.helper.remove();return false}});b.extend(b.ui.selectable,{version:"1.8.11"})})(jQuery);
(function(b){b.widget("ui.sortable",b.ui.mouse,{widgetEventPrefix:"sort",options:{appendTo:"parent",axis:false,connectWith:false,containment:false,cursor:"auto",cursorAt:false,dropOnEmpty:true,forcePlaceholderSize:false,forceHelperSize:false,grid:false,handle:false,helper:"original",items:"> *",opacity:false,placeholder:false,revert:false,scroll:true,scrollSensitivity:20,scrollSpeed:20,scope:"default",tolerance:"intersect",zIndex:1E3},_create:function(){this.containerCache={};this.element.addClass("ui-sortable");
this.refresh();this.floating=this.items.length?/left|right/.test(this.items[0].item.css("float"))||/inline|table-cell/.test(this.items[0].item.css("display")):false;this.offset=this.element.offset();this._mouseInit()},destroy:function(){this.element.removeClass("ui-sortable ui-sortable-disabled").removeData("sortable").unbind(".sortable");this._mouseDestroy();for(var d=this.items.length-1;d>=0;d--)this.items[d].item.removeData("sortable-item");return this},_setOption:function(d,e){if(d==="disabled"){this.options[d]=
e;this.widget()[e?"addClass":"removeClass"]("ui-sortable-disabled")}else b.Widget.prototype._setOption.apply(this,arguments)},_mouseCapture:function(d,e){if(this.reverting)return false;if(this.options.disabled||this.options.type=="static")return false;this._refreshItems(d);var g=null,f=this;b(d.target).parents().each(function(){if(b.data(this,"sortable-item")==f){g=b(this);return false}});if(b.data(d.target,"sortable-item")==f)g=b(d.target);if(!g)return false;if(this.options.handle&&!e){var a=false;
b(this.options.handle,g).find("*").andSelf().each(function(){if(this==d.target)a=true});if(!a)return false}this.currentItem=g;this._removeCurrentsFromItems();return true},_mouseStart:function(d,e,g){e=this.options;var f=this;this.currentContainer=this;this.refreshPositions();this.helper=this._createHelper(d);this._cacheHelperProportions();this._cacheMargins();this.scrollParent=this.helper.scrollParent();this.offset=this.currentItem.offset();this.offset={top:this.offset.top-this.margins.top,left:this.offset.left-
this.margins.left};this.helper.css("position","absolute");this.cssPosition=this.helper.css("position");b.extend(this.offset,{click:{left:d.pageX-this.offset.left,top:d.pageY-this.offset.top},parent:this._getParentOffset(),relative:this._getRelativeOffset()});this.originalPosition=this._generatePosition(d);this.originalPageX=d.pageX;this.originalPageY=d.pageY;e.cursorAt&&this._adjustOffsetFromHelper(e.cursorAt);this.domPosition={prev:this.currentItem.prev()[0],parent:this.currentItem.parent()[0]};
this.helper[0]!=this.currentItem[0]&&this.currentItem.hide();this._createPlaceholder();e.containment&&this._setContainment();if(e.cursor){if(b("body").css("cursor"))this._storedCursor=b("body").css("cursor");b("body").css("cursor",e.cursor)}if(e.opacity){if(this.helper.css("opacity"))this._storedOpacity=this.helper.css("opacity");this.helper.css("opacity",e.opacity)}if(e.zIndex){if(this.helper.css("zIndex"))this._storedZIndex=this.helper.css("zIndex");this.helper.css("zIndex",e.zIndex)}if(this.scrollParent[0]!=
document&&this.scrollParent[0].tagName!="HTML")this.overflowOffset=this.scrollParent.offset();this._trigger("start",d,this._uiHash());this._preserveHelperProportions||this._cacheHelperProportions();if(!g)for(g=this.containers.length-1;g>=0;g--)this.containers[g]._trigger("activate",d,f._uiHash(this));if(b.ui.ddmanager)b.ui.ddmanager.current=this;b.ui.ddmanager&&!e.dropBehaviour&&b.ui.ddmanager.prepareOffsets(this,d);this.dragging=true;this.helper.addClass("ui-sortable-helper");this._mouseDrag(d);
return true},_mouseDrag:function(d){this.position=this._generatePosition(d);this.positionAbs=this._convertPositionTo("absolute");if(!this.lastPositionAbs)this.lastPositionAbs=this.positionAbs;if(this.options.scroll){var e=this.options,g=false;if(this.scrollParent[0]!=document&&this.scrollParent[0].tagName!="HTML"){if(this.overflowOffset.top+this.scrollParent[0].offsetHeight-d.pageY<e.scrollSensitivity)this.scrollParent[0].scrollTop=g=this.scrollParent[0].scrollTop+e.scrollSpeed;else if(d.pageY-this.overflowOffset.top<
e.scrollSensitivity)this.scrollParent[0].scrollTop=g=this.scrollParent[0].scrollTop-e.scrollSpeed;if(this.overflowOffset.left+this.scrollParent[0].offsetWidth-d.pageX<e.scrollSensitivity)this.scrollParent[0].scrollLeft=g=this.scrollParent[0].scrollLeft+e.scrollSpeed;else if(d.pageX-this.overflowOffset.left<e.scrollSensitivity)this.scrollParent[0].scrollLeft=g=this.scrollParent[0].scrollLeft-e.scrollSpeed}else{if(d.pageY-b(document).scrollTop()<e.scrollSensitivity)g=b(document).scrollTop(b(document).scrollTop()-
e.scrollSpeed);else if(b(window).height()-(d.pageY-b(document).scrollTop())<e.scrollSensitivity)g=b(document).scrollTop(b(document).scrollTop()+e.scrollSpeed);if(d.pageX-b(document).scrollLeft()<e.scrollSensitivity)g=b(document).scrollLeft(b(document).scrollLeft()-e.scrollSpeed);else if(b(window).width()-(d.pageX-b(document).scrollLeft())<e.scrollSensitivity)g=b(document).scrollLeft(b(document).scrollLeft()+e.scrollSpeed)}g!==false&&b.ui.ddmanager&&!e.dropBehaviour&&b.ui.ddmanager.prepareOffsets(this,
d)}this.positionAbs=this._convertPositionTo("absolute");if(!this.options.axis||this.options.axis!="y")this.helper[0].style.left=this.position.left+"px";if(!this.options.axis||this.options.axis!="x")this.helper[0].style.top=this.position.top+"px";for(e=this.items.length-1;e>=0;e--){g=this.items[e];var f=g.item[0],a=this._intersectsWithPointer(g);if(a)if(f!=this.currentItem[0]&&this.placeholder[a==1?"next":"prev"]()[0]!=f&&!b.ui.contains(this.placeholder[0],f)&&(this.options.type=="semi-dynamic"?!b.ui.contains(this.element[0],
f):true)){this.direction=a==1?"down":"up";if(this.options.tolerance=="pointer"||this._intersectsWithSides(g))this._rearrange(d,g);else break;this._trigger("change",d,this._uiHash());break}}this._contactContainers(d);b.ui.ddmanager&&b.ui.ddmanager.drag(this,d);this._trigger("sort",d,this._uiHash());this.lastPositionAbs=this.positionAbs;return false},_mouseStop:function(d,e){if(d){b.ui.ddmanager&&!this.options.dropBehaviour&&b.ui.ddmanager.drop(this,d);if(this.options.revert){var g=this;e=g.placeholder.offset();
g.reverting=true;b(this.helper).animate({left:e.left-this.offset.parent.left-g.margins.left+(this.offsetParent[0]==document.body?0:this.offsetParent[0].scrollLeft),top:e.top-this.offset.parent.top-g.margins.top+(this.offsetParent[0]==document.body?0:this.offsetParent[0].scrollTop)},parseInt(this.options.revert,10)||500,function(){g._clear(d)})}else this._clear(d,e);return false}},cancel:function(){var d=this;if(this.dragging){this._mouseUp({target:null});this.options.helper=="original"?this.currentItem.css(this._storedCSS).removeClass("ui-sortable-helper"):
this.currentItem.show();for(var e=this.containers.length-1;e>=0;e--){this.containers[e]._trigger("deactivate",null,d._uiHash(this));if(this.containers[e].containerCache.over){this.containers[e]._trigger("out",null,d._uiHash(this));this.containers[e].containerCache.over=0}}}if(this.placeholder){this.placeholder[0].parentNode&&this.placeholder[0].parentNode.removeChild(this.placeholder[0]);this.options.helper!="original"&&this.helper&&this.helper[0].parentNode&&this.helper.remove();b.extend(this,{helper:null,
dragging:false,reverting:false,_noFinalSort:null});this.domPosition.prev?b(this.domPosition.prev).after(this.currentItem):b(this.domPosition.parent).prepend(this.currentItem)}return this},serialize:function(d){var e=this._getItemsAsjQuery(d&&d.connected),g=[];d=d||{};b(e).each(function(){var f=(b(d.item||this).attr(d.attribute||"id")||"").match(d.expression||/(.+)[-=_](.+)/);if(f)g.push((d.key||f[1]+"[]")+"="+(d.key&&d.expression?f[1]:f[2]))});!g.length&&d.key&&g.push(d.key+"=");return g.join("&")},
toArray:function(d){var e=this._getItemsAsjQuery(d&&d.connected),g=[];d=d||{};e.each(function(){g.push(b(d.item||this).attr(d.attribute||"id")||"")});return g},_intersectsWith:function(d){var e=this.positionAbs.left,g=e+this.helperProportions.width,f=this.positionAbs.top,a=f+this.helperProportions.height,c=d.left,h=c+d.width,i=d.top,j=i+d.height,n=this.offset.click.top,p=this.offset.click.left;n=f+n>i&&f+n<j&&e+p>c&&e+p<h;return this.options.tolerance=="pointer"||this.options.forcePointerForContainers||
this.options.tolerance!="pointer"&&this.helperProportions[this.floating?"width":"height"]>d[this.floating?"width":"height"]?n:c<e+this.helperProportions.width/2&&g-this.helperProportions.width/2<h&&i<f+this.helperProportions.height/2&&a-this.helperProportions.height/2<j},_intersectsWithPointer:function(d){var e=b.ui.isOverAxis(this.positionAbs.top+this.offset.click.top,d.top,d.height);d=b.ui.isOverAxis(this.positionAbs.left+this.offset.click.left,d.left,d.width);e=e&&d;d=this._getDragVerticalDirection();
var g=this._getDragHorizontalDirection();if(!e)return false;return this.floating?g&&g=="right"||d=="down"?2:1:d&&(d=="down"?2:1)},_intersectsWithSides:function(d){var e=b.ui.isOverAxis(this.positionAbs.top+this.offset.click.top,d.top+d.height/2,d.height);d=b.ui.isOverAxis(this.positionAbs.left+this.offset.click.left,d.left+d.width/2,d.width);var g=this._getDragVerticalDirection(),f=this._getDragHorizontalDirection();return this.floating&&f?f=="right"&&d||f=="left"&&!d:g&&(g=="down"&&e||g=="up"&&!e)},
_getDragVerticalDirection:function(){var d=this.positionAbs.top-this.lastPositionAbs.top;return d!=0&&(d>0?"down":"up")},_getDragHorizontalDirection:function(){var d=this.positionAbs.left-this.lastPositionAbs.left;return d!=0&&(d>0?"right":"left")},refresh:function(d){this._refreshItems(d);this.refreshPositions();return this},_connectWith:function(){var d=this.options;return d.connectWith.constructor==String?[d.connectWith]:d.connectWith},_getItemsAsjQuery:function(d){var e=[],g=[],f=this._connectWith();
if(f&&d)for(d=f.length-1;d>=0;d--)for(var a=b(f[d]),c=a.length-1;c>=0;c--){var h=b.data(a[c],"sortable");if(h&&h!=this&&!h.options.disabled)g.push([b.isFunction(h.options.items)?h.options.items.call(h.element):b(h.options.items,h.element).not(".ui-sortable-helper").not(".ui-sortable-placeholder"),h])}g.push([b.isFunction(this.options.items)?this.options.items.call(this.element,null,{options:this.options,item:this.currentItem}):b(this.options.items,this.element).not(".ui-sortable-helper").not(".ui-sortable-placeholder"),
this]);for(d=g.length-1;d>=0;d--)g[d][0].each(function(){e.push(this)});return b(e)},_removeCurrentsFromItems:function(){for(var d=this.currentItem.find(":data(sortable-item)"),e=0;e<this.items.length;e++)for(var g=0;g<d.length;g++)d[g]==this.items[e].item[0]&&this.items.splice(e,1)},_refreshItems:function(d){this.items=[];this.containers=[this];var e=this.items,g=[[b.isFunction(this.options.items)?this.options.items.call(this.element[0],d,{item:this.currentItem}):b(this.options.items,this.element),
this]],f=this._connectWith();if(f)for(var a=f.length-1;a>=0;a--)for(var c=b(f[a]),h=c.length-1;h>=0;h--){var i=b.data(c[h],"sortable");if(i&&i!=this&&!i.options.disabled){g.push([b.isFunction(i.options.items)?i.options.items.call(i.element[0],d,{item:this.currentItem}):b(i.options.items,i.element),i]);this.containers.push(i)}}for(a=g.length-1;a>=0;a--){d=g[a][1];f=g[a][0];h=0;for(c=f.length;h<c;h++){i=b(f[h]);i.data("sortable-item",d);e.push({item:i,instance:d,width:0,height:0,left:0,top:0})}}},refreshPositions:function(d){if(this.offsetParent&&
this.helper)this.offset.parent=this._getParentOffset();for(var e=this.items.length-1;e>=0;e--){var g=this.items[e],f=this.options.toleranceElement?b(this.options.toleranceElement,g.item):g.item;if(!d){g.width=f.outerWidth();g.height=f.outerHeight()}f=f.offset();g.left=f.left;g.top=f.top}if(this.options.custom&&this.options.custom.refreshContainers)this.options.custom.refreshContainers.call(this);else for(e=this.containers.length-1;e>=0;e--){f=this.containers[e].element.offset();this.containers[e].containerCache.left=
f.left;this.containers[e].containerCache.top=f.top;this.containers[e].containerCache.width=this.containers[e].element.outerWidth();this.containers[e].containerCache.height=this.containers[e].element.outerHeight()}return this},_createPlaceholder:function(d){var e=d||this,g=e.options;if(!g.placeholder||g.placeholder.constructor==String){var f=g.placeholder;g.placeholder={element:function(){var a=b(document.createElement(e.currentItem[0].nodeName)).addClass(f||e.currentItem[0].className+" ui-sortable-placeholder").removeClass("ui-sortable-helper")[0];
if(!f)a.style.visibility="hidden";return a},update:function(a,c){if(!(f&&!g.forcePlaceholderSize)){c.height()||c.height(e.currentItem.innerHeight()-parseInt(e.currentItem.css("paddingTop")||0,10)-parseInt(e.currentItem.css("paddingBottom")||0,10));c.width()||c.width(e.currentItem.innerWidth()-parseInt(e.currentItem.css("paddingLeft")||0,10)-parseInt(e.currentItem.css("paddingRight")||0,10))}}}}e.placeholder=b(g.placeholder.element.call(e.element,e.currentItem));e.currentItem.after(e.placeholder);
g.placeholder.update(e,e.placeholder)},_contactContainers:function(d){for(var e=null,g=null,f=this.containers.length-1;f>=0;f--)if(!b.ui.contains(this.currentItem[0],this.containers[f].element[0]))if(this._intersectsWith(this.containers[f].containerCache)){if(!(e&&b.ui.contains(this.containers[f].element[0],e.element[0]))){e=this.containers[f];g=f}}else if(this.containers[f].containerCache.over){this.containers[f]._trigger("out",d,this._uiHash(this));this.containers[f].containerCache.over=0}if(e)if(this.containers.length===
1){this.containers[g]._trigger("over",d,this._uiHash(this));this.containers[g].containerCache.over=1}else if(this.currentContainer!=this.containers[g]){e=1E4;f=null;for(var a=this.positionAbs[this.containers[g].floating?"left":"top"],c=this.items.length-1;c>=0;c--)if(b.ui.contains(this.containers[g].element[0],this.items[c].item[0])){var h=this.items[c][this.containers[g].floating?"left":"top"];if(Math.abs(h-a)<e){e=Math.abs(h-a);f=this.items[c]}}if(f||this.options.dropOnEmpty){this.currentContainer=
this.containers[g];f?this._rearrange(d,f,null,true):this._rearrange(d,null,this.containers[g].element,true);this._trigger("change",d,this._uiHash());this.containers[g]._trigger("change",d,this._uiHash(this));this.options.placeholder.update(this.currentContainer,this.placeholder);this.containers[g]._trigger("over",d,this._uiHash(this));this.containers[g].containerCache.over=1}}},_createHelper:function(d){var e=this.options;d=b.isFunction(e.helper)?b(e.helper.apply(this.element[0],[d,this.currentItem])):
e.helper=="clone"?this.currentItem.clone():this.currentItem;d.parents("body").length||b(e.appendTo!="parent"?e.appendTo:this.currentItem[0].parentNode)[0].appendChild(d[0]);if(d[0]==this.currentItem[0])this._storedCSS={width:this.currentItem[0].style.width,height:this.currentItem[0].style.height,position:this.currentItem.css("position"),top:this.currentItem.css("top"),left:this.currentItem.css("left")};if(d[0].style.width==""||e.forceHelperSize)d.width(this.currentItem.width());if(d[0].style.height==
""||e.forceHelperSize)d.height(this.currentItem.height());return d},_adjustOffsetFromHelper:function(d){if(typeof d=="string")d=d.split(" ");if(b.isArray(d))d={left:+d[0],top:+d[1]||0};if("left"in d)this.offset.click.left=d.left+this.margins.left;if("right"in d)this.offset.click.left=this.helperProportions.width-d.right+this.margins.left;if("top"in d)this.offset.click.top=d.top+this.margins.top;if("bottom"in d)this.offset.click.top=this.helperProportions.height-d.bottom+this.margins.top},_getParentOffset:function(){this.offsetParent=
this.helper.offsetParent();var d=this.offsetParent.offset();if(this.cssPosition=="absolute"&&this.scrollParent[0]!=document&&b.ui.contains(this.scrollParent[0],this.offsetParent[0])){d.left+=this.scrollParent.scrollLeft();d.top+=this.scrollParent.scrollTop()}if(this.offsetParent[0]==document.body||this.offsetParent[0].tagName&&this.offsetParent[0].tagName.toLowerCase()=="html"&&b.browser.msie)d={top:0,left:0};return{top:d.top+(parseInt(this.offsetParent.css("borderTopWidth"),10)||0),left:d.left+(parseInt(this.offsetParent.css("borderLeftWidth"),
10)||0)}},_getRelativeOffset:function(){if(this.cssPosition=="relative"){var d=this.currentItem.position();return{top:d.top-(parseInt(this.helper.css("top"),10)||0)+this.scrollParent.scrollTop(),left:d.left-(parseInt(this.helper.css("left"),10)||0)+this.scrollParent.scrollLeft()}}else return{top:0,left:0}},_cacheMargins:function(){this.margins={left:parseInt(this.currentItem.css("marginLeft"),10)||0,top:parseInt(this.currentItem.css("marginTop"),10)||0}},_cacheHelperProportions:function(){this.helperProportions=
{width:this.helper.outerWidth(),height:this.helper.outerHeight()}},_setContainment:function(){var d=this.options;if(d.containment=="parent")d.containment=this.helper[0].parentNode;if(d.containment=="document"||d.containment=="window")this.containment=[0-this.offset.relative.left-this.offset.parent.left,0-this.offset.relative.top-this.offset.parent.top,b(d.containment=="document"?document:window).width()-this.helperProportions.width-this.margins.left,(b(d.containment=="document"?document:window).height()||
document.body.parentNode.scrollHeight)-this.helperProportions.height-this.margins.top];if(!/^(document|window|parent)$/.test(d.containment)){var e=b(d.containment)[0];d=b(d.containment).offset();var g=b(e).css("overflow")!="hidden";this.containment=[d.left+(parseInt(b(e).css("borderLeftWidth"),10)||0)+(parseInt(b(e).css("paddingLeft"),10)||0)-this.margins.left,d.top+(parseInt(b(e).css("borderTopWidth"),10)||0)+(parseInt(b(e).css("paddingTop"),10)||0)-this.margins.top,d.left+(g?Math.max(e.scrollWidth,
e.offsetWidth):e.offsetWidth)-(parseInt(b(e).css("borderLeftWidth"),10)||0)-(parseInt(b(e).css("paddingRight"),10)||0)-this.helperProportions.width-this.margins.left,d.top+(g?Math.max(e.scrollHeight,e.offsetHeight):e.offsetHeight)-(parseInt(b(e).css("borderTopWidth"),10)||0)-(parseInt(b(e).css("paddingBottom"),10)||0)-this.helperProportions.height-this.margins.top]}},_convertPositionTo:function(d,e){if(!e)e=this.position;d=d=="absolute"?1:-1;var g=this.cssPosition=="absolute"&&!(this.scrollParent[0]!=
document&&b.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,f=/(html|body)/i.test(g[0].tagName);return{top:e.top+this.offset.relative.top*d+this.offset.parent.top*d-(b.browser.safari&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollTop():f?0:g.scrollTop())*d),left:e.left+this.offset.relative.left*d+this.offset.parent.left*d-(b.browser.safari&&this.cssPosition=="fixed"?0:(this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():
f?0:g.scrollLeft())*d)}},_generatePosition:function(d){var e=this.options,g=this.cssPosition=="absolute"&&!(this.scrollParent[0]!=document&&b.ui.contains(this.scrollParent[0],this.offsetParent[0]))?this.offsetParent:this.scrollParent,f=/(html|body)/i.test(g[0].tagName);if(this.cssPosition=="relative"&&!(this.scrollParent[0]!=document&&this.scrollParent[0]!=this.offsetParent[0]))this.offset.relative=this._getRelativeOffset();var a=d.pageX,c=d.pageY;if(this.originalPosition){if(this.containment){if(d.pageX-
this.offset.click.left<this.containment[0])a=this.containment[0]+this.offset.click.left;if(d.pageY-this.offset.click.top<this.containment[1])c=this.containment[1]+this.offset.click.top;if(d.pageX-this.offset.click.left>this.containment[2])a=this.containment[2]+this.offset.click.left;if(d.pageY-this.offset.click.top>this.containment[3])c=this.containment[3]+this.offset.click.top}if(e.grid){c=this.originalPageY+Math.round((c-this.originalPageY)/e.grid[1])*e.grid[1];c=this.containment?!(c-this.offset.click.top<
this.containment[1]||c-this.offset.click.top>this.containment[3])?c:!(c-this.offset.click.top<this.containment[1])?c-e.grid[1]:c+e.grid[1]:c;a=this.originalPageX+Math.round((a-this.originalPageX)/e.grid[0])*e.grid[0];a=this.containment?!(a-this.offset.click.left<this.containment[0]||a-this.offset.click.left>this.containment[2])?a:!(a-this.offset.click.left<this.containment[0])?a-e.grid[0]:a+e.grid[0]:a}}return{top:c-this.offset.click.top-this.offset.relative.top-this.offset.parent.top+(b.browser.safari&&
this.cssPosition=="fixed"?0:this.cssPosition=="fixed"?-this.scrollParent.scrollTop():f?0:g.scrollTop()),left:a-this.offset.click.left-this.offset.relative.left-this.offset.parent.left+(b.browser.safari&&this.cssPosition=="fixed"?0:this.cssPosition=="fixed"?-this.scrollParent.scrollLeft():f?0:g.scrollLeft())}},_rearrange:function(d,e,g,f){g?g[0].appendChild(this.placeholder[0]):e.item[0].parentNode.insertBefore(this.placeholder[0],this.direction=="down"?e.item[0]:e.item[0].nextSibling);this.counter=
this.counter?++this.counter:1;var a=this,c=this.counter;window.setTimeout(function(){c==a.counter&&a.refreshPositions(!f)},0)},_clear:function(d,e){this.reverting=false;var g=[];!this._noFinalSort&&this.currentItem[0].parentNode&&this.placeholder.before(this.currentItem);this._noFinalSort=null;if(this.helper[0]==this.currentItem[0]){for(var f in this._storedCSS)if(this._storedCSS[f]=="auto"||this._storedCSS[f]=="static")this._storedCSS[f]="";this.currentItem.css(this._storedCSS).removeClass("ui-sortable-helper")}else this.currentItem.show();
this.fromOutside&&!e&&g.push(function(a){this._trigger("receive",a,this._uiHash(this.fromOutside))});if((this.fromOutside||this.domPosition.prev!=this.currentItem.prev().not(".ui-sortable-helper")[0]||this.domPosition.parent!=this.currentItem.parent()[0])&&!e)g.push(function(a){this._trigger("update",a,this._uiHash())});if(!b.ui.contains(this.element[0],this.currentItem[0])){e||g.push(function(a){this._trigger("remove",a,this._uiHash())});for(f=this.containers.length-1;f>=0;f--)if(b.ui.contains(this.containers[f].element[0],
this.currentItem[0])&&!e){g.push(function(a){return function(c){a._trigger("receive",c,this._uiHash(this))}}.call(this,this.containers[f]));g.push(function(a){return function(c){a._trigger("update",c,this._uiHash(this))}}.call(this,this.containers[f]))}}for(f=this.containers.length-1;f>=0;f--){e||g.push(function(a){return function(c){a._trigger("deactivate",c,this._uiHash(this))}}.call(this,this.containers[f]));if(this.containers[f].containerCache.over){g.push(function(a){return function(c){a._trigger("out",
c,this._uiHash(this))}}.call(this,this.containers[f]));this.containers[f].containerCache.over=0}}this._storedCursor&&b("body").css("cursor",this._storedCursor);this._storedOpacity&&this.helper.css("opacity",this._storedOpacity);if(this._storedZIndex)this.helper.css("zIndex",this._storedZIndex=="auto"?"":this._storedZIndex);this.dragging=false;if(this.cancelHelperRemoval){if(!e){this._trigger("beforeStop",d,this._uiHash());for(f=0;f<g.length;f++)g[f].call(this,d);this._trigger("stop",d,this._uiHash())}return false}e||
this._trigger("beforeStop",d,this._uiHash());this.placeholder[0].parentNode.removeChild(this.placeholder[0]);this.helper[0]!=this.currentItem[0]&&this.helper.remove();this.helper=null;if(!e){for(f=0;f<g.length;f++)g[f].call(this,d);this._trigger("stop",d,this._uiHash())}this.fromOutside=false;return true},_trigger:function(){b.Widget.prototype._trigger.apply(this,arguments)===false&&this.cancel()},_uiHash:function(d){var e=d||this;return{helper:e.helper,placeholder:e.placeholder||b([]),position:e.position,
originalPosition:e.originalPosition,offset:e.positionAbs,item:e.currentItem,sender:d?d.element:null}}});b.extend(b.ui.sortable,{version:"1.8.11"})})(jQuery);
jQuery.effects||function(b,d){function e(l){var k;if(l&&l.constructor==Array&&l.length==3)return l;if(k=/rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(l))return[parseInt(k[1],10),parseInt(k[2],10),parseInt(k[3],10)];if(k=/rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(l))return[parseFloat(k[1])*2.55,parseFloat(k[2])*2.55,parseFloat(k[3])*2.55];if(k=/#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(l))return[parseInt(k[1],
16),parseInt(k[2],16),parseInt(k[3],16)];if(k=/#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(l))return[parseInt(k[1]+k[1],16),parseInt(k[2]+k[2],16),parseInt(k[3]+k[3],16)];if(/rgba\(0, 0, 0, 0\)/.exec(l))return j.transparent;return j[b.trim(l).toLowerCase()]}function g(l,k){var m;do{m=b.curCSS(l,k);if(m!=""&&m!="transparent"||b.nodeName(l,"body"))break;k="backgroundColor"}while(l=l.parentNode);return e(m)}function f(){var l=document.defaultView?document.defaultView.getComputedStyle(this,null):this.currentStyle,
k={},m,o;if(l&&l.length&&l[0]&&l[l[0]])for(var q=l.length;q--;){m=l[q];if(typeof l[m]=="string"){o=m.replace(/\-(\w)/g,function(s,r){return r.toUpperCase()});k[o]=l[m]}}else for(m in l)if(typeof l[m]==="string")k[m]=l[m];return k}function a(l){var k,m;for(k in l){m=l[k];if(m==null||b.isFunction(m)||k in p||/scrollbar/.test(k)||!/color/i.test(k)&&isNaN(parseFloat(m)))delete l[k]}return l}function c(l,k){var m={_:0},o;for(o in k)if(l[o]!=k[o])m[o]=k[o];return m}function h(l,k,m,o){if(typeof l=="object"){o=
k;m=null;k=l;l=k.effect}if(b.isFunction(k)){o=k;m=null;k={}}if(typeof k=="number"||b.fx.speeds[k]){o=m;m=k;k={}}if(b.isFunction(m)){o=m;m=null}k=k||{};m=m||k.duration;m=b.fx.off?0:typeof m=="number"?m:m in b.fx.speeds?b.fx.speeds[m]:b.fx.speeds._default;o=o||k.complete;return[l,k,m,o]}function i(l){if(!l||typeof l==="number"||b.fx.speeds[l])return true;if(typeof l==="string"&&!b.effects[l])return true;return false}b.effects={};b.each(["backgroundColor","borderBottomColor","borderLeftColor","borderRightColor",
"borderTopColor","borderColor","color","outlineColor"],function(l,k){b.fx.step[k]=function(m){if(!m.colorInit){m.start=g(m.elem,k);m.end=e(m.end);m.colorInit=true}m.elem.style[k]="rgb("+Math.max(Math.min(parseInt(m.pos*(m.end[0]-m.start[0])+m.start[0],10),255),0)+","+Math.max(Math.min(parseInt(m.pos*(m.end[1]-m.start[1])+m.start[1],10),255),0)+","+Math.max(Math.min(parseInt(m.pos*(m.end[2]-m.start[2])+m.start[2],10),255),0)+")"}});var j={aqua:[0,255,255],azure:[240,255,255],beige:[245,245,220],black:[0,
0,0],blue:[0,0,255],brown:[165,42,42],cyan:[0,255,255],darkblue:[0,0,139],darkcyan:[0,139,139],darkgrey:[169,169,169],darkgreen:[0,100,0],darkkhaki:[189,183,107],darkmagenta:[139,0,139],darkolivegreen:[85,107,47],darkorange:[255,140,0],darkorchid:[153,50,204],darkred:[139,0,0],darksalmon:[233,150,122],darkviolet:[148,0,211],fuchsia:[255,0,255],gold:[255,215,0],green:[0,128,0],indigo:[75,0,130],khaki:[240,230,140],lightblue:[173,216,230],lightcyan:[224,255,255],lightgreen:[144,238,144],lightgrey:[211,
211,211],lightpink:[255,182,193],lightyellow:[255,255,224],lime:[0,255,0],magenta:[255,0,255],maroon:[128,0,0],navy:[0,0,128],olive:[128,128,0],orange:[255,165,0],pink:[255,192,203],purple:[128,0,128],violet:[128,0,128],red:[255,0,0],silver:[192,192,192],white:[255,255,255],yellow:[255,255,0],transparent:[255,255,255]},n=["add","remove","toggle"],p={border:1,borderBottom:1,borderColor:1,borderLeft:1,borderRight:1,borderTop:1,borderWidth:1,margin:1,padding:1};b.effects.animateClass=function(l,k,m,
o){if(b.isFunction(m)){o=m;m=null}return this.queue("fx",function(){var q=b(this),s=q.attr("style")||" ",r=a(f.call(this)),u,v=q.attr("className");b.each(n,function(w,y){l[y]&&q[y+"Class"](l[y])});u=a(f.call(this));q.attr("className",v);q.animate(c(r,u),k,m,function(){b.each(n,function(w,y){l[y]&&q[y+"Class"](l[y])});if(typeof q.attr("style")=="object"){q.attr("style").cssText="";q.attr("style").cssText=s}else q.attr("style",s);o&&o.apply(this,arguments)});r=b.queue(this);u=r.splice(r.length-1,1)[0];
r.splice(1,0,u);b.dequeue(this)})};b.fn.extend({_addClass:b.fn.addClass,addClass:function(l,k,m,o){return k?b.effects.animateClass.apply(this,[{add:l},k,m,o]):this._addClass(l)},_removeClass:b.fn.removeClass,removeClass:function(l,k,m,o){return k?b.effects.animateClass.apply(this,[{remove:l},k,m,o]):this._removeClass(l)},_toggleClass:b.fn.toggleClass,toggleClass:function(l,k,m,o,q){return typeof k=="boolean"||k===d?m?b.effects.animateClass.apply(this,[k?{add:l}:{remove:l},m,o,q]):this._toggleClass(l,
k):b.effects.animateClass.apply(this,[{toggle:l},k,m,o])},switchClass:function(l,k,m,o,q){return b.effects.animateClass.apply(this,[{add:k,remove:l},m,o,q])}});b.extend(b.effects,{version:"1.8.11",save:function(l,k){for(var m=0;m<k.length;m++)k[m]!==null&&l.data("ec.storage."+k[m],l[0].style[k[m]])},restore:function(l,k){for(var m=0;m<k.length;m++)k[m]!==null&&l.css(k[m],l.data("ec.storage."+k[m]))},setMode:function(l,k){if(k=="toggle")k=l.is(":hidden")?"show":"hide";return k},getBaseline:function(l,
k){var m;switch(l[0]){case "top":m=0;break;case "middle":m=0.5;break;case "bottom":m=1;break;default:m=l[0]/k.height}switch(l[1]){case "left":l=0;break;case "center":l=0.5;break;case "right":l=1;break;default:l=l[1]/k.width}return{x:l,y:m}},createWrapper:function(l){if(l.parent().is(".ui-effects-wrapper"))return l.parent();var k={width:l.outerWidth(true),height:l.outerHeight(true),"float":l.css("float")},m=b("<div></div>").addClass("ui-effects-wrapper").css({fontSize:"100%",background:"transparent",
border:"none",margin:0,padding:0});l.wrap(m);m=l.parent();if(l.css("position")=="static"){m.css({position:"relative"});l.css({position:"relative"})}else{b.extend(k,{position:l.css("position"),zIndex:l.css("z-index")});b.each(["top","left","bottom","right"],function(o,q){k[q]=l.css(q);if(isNaN(parseInt(k[q],10)))k[q]="auto"});l.css({position:"relative",top:0,left:0,right:"auto",bottom:"auto"})}return m.css(k).show()},removeWrapper:function(l){if(l.parent().is(".ui-effects-wrapper"))return l.parent().replaceWith(l);
return l},setTransition:function(l,k,m,o){o=o||{};b.each(k,function(q,s){unit=l.cssUnit(s);if(unit[0]>0)o[s]=unit[0]*m+unit[1]});return o}});b.fn.extend({effect:function(l){var k=h.apply(this,arguments),m={options:k[1],duration:k[2],callback:k[3]};k=m.options.mode;var o=b.effects[l];if(b.fx.off||!o)return k?this[k](m.duration,m.callback):this.each(function(){m.callback&&m.callback.call(this)});return o.call(this,m)},_show:b.fn.show,show:function(l){if(i(l))return this._show.apply(this,arguments);
else{var k=h.apply(this,arguments);k[1].mode="show";return this.effect.apply(this,k)}},_hide:b.fn.hide,hide:function(l){if(i(l))return this._hide.apply(this,arguments);else{var k=h.apply(this,arguments);k[1].mode="hide";return this.effect.apply(this,k)}},__toggle:b.fn.toggle,toggle:function(l){if(i(l)||typeof l==="boolean"||b.isFunction(l))return this.__toggle.apply(this,arguments);else{var k=h.apply(this,arguments);k[1].mode="toggle";return this.effect.apply(this,k)}},cssUnit:function(l){var k=this.css(l),
m=[];b.each(["em","px","%","pt"],function(o,q){if(k.indexOf(q)>0)m=[parseFloat(k),q]});return m}});b.easing.jswing=b.easing.swing;b.extend(b.easing,{def:"easeOutQuad",swing:function(l,k,m,o,q){return b.easing[b.easing.def](l,k,m,o,q)},easeInQuad:function(l,k,m,o,q){return o*(k/=q)*k+m},easeOutQuad:function(l,k,m,o,q){return-o*(k/=q)*(k-2)+m},easeInOutQuad:function(l,k,m,o,q){if((k/=q/2)<1)return o/2*k*k+m;return-o/2*(--k*(k-2)-1)+m},easeInCubic:function(l,k,m,o,q){return o*(k/=q)*k*k+m},easeOutCubic:function(l,
k,m,o,q){return o*((k=k/q-1)*k*k+1)+m},easeInOutCubic:function(l,k,m,o,q){if((k/=q/2)<1)return o/2*k*k*k+m;return o/2*((k-=2)*k*k+2)+m},easeInQuart:function(l,k,m,o,q){return o*(k/=q)*k*k*k+m},easeOutQuart:function(l,k,m,o,q){return-o*((k=k/q-1)*k*k*k-1)+m},easeInOutQuart:function(l,k,m,o,q){if((k/=q/2)<1)return o/2*k*k*k*k+m;return-o/2*((k-=2)*k*k*k-2)+m},easeInQuint:function(l,k,m,o,q){return o*(k/=q)*k*k*k*k+m},easeOutQuint:function(l,k,m,o,q){return o*((k=k/q-1)*k*k*k*k+1)+m},easeInOutQuint:function(l,
k,m,o,q){if((k/=q/2)<1)return o/2*k*k*k*k*k+m;return o/2*((k-=2)*k*k*k*k+2)+m},easeInSine:function(l,k,m,o,q){return-o*Math.cos(k/q*(Math.PI/2))+o+m},easeOutSine:function(l,k,m,o,q){return o*Math.sin(k/q*(Math.PI/2))+m},easeInOutSine:function(l,k,m,o,q){return-o/2*(Math.cos(Math.PI*k/q)-1)+m},easeInExpo:function(l,k,m,o,q){return k==0?m:o*Math.pow(2,10*(k/q-1))+m},easeOutExpo:function(l,k,m,o,q){return k==q?m+o:o*(-Math.pow(2,-10*k/q)+1)+m},easeInOutExpo:function(l,k,m,o,q){if(k==0)return m;if(k==
q)return m+o;if((k/=q/2)<1)return o/2*Math.pow(2,10*(k-1))+m;return o/2*(-Math.pow(2,-10*--k)+2)+m},easeInCirc:function(l,k,m,o,q){return-o*(Math.sqrt(1-(k/=q)*k)-1)+m},easeOutCirc:function(l,k,m,o,q){return o*Math.sqrt(1-(k=k/q-1)*k)+m},easeInOutCirc:function(l,k,m,o,q){if((k/=q/2)<1)return-o/2*(Math.sqrt(1-k*k)-1)+m;return o/2*(Math.sqrt(1-(k-=2)*k)+1)+m},easeInElastic:function(l,k,m,o,q){l=1.70158;var s=0,r=o;if(k==0)return m;if((k/=q)==1)return m+o;s||(s=q*0.3);if(r<Math.abs(o)){r=o;l=s/4}else l=
s/(2*Math.PI)*Math.asin(o/r);return-(r*Math.pow(2,10*(k-=1))*Math.sin((k*q-l)*2*Math.PI/s))+m},easeOutElastic:function(l,k,m,o,q){l=1.70158;var s=0,r=o;if(k==0)return m;if((k/=q)==1)return m+o;s||(s=q*0.3);if(r<Math.abs(o)){r=o;l=s/4}else l=s/(2*Math.PI)*Math.asin(o/r);return r*Math.pow(2,-10*k)*Math.sin((k*q-l)*2*Math.PI/s)+o+m},easeInOutElastic:function(l,k,m,o,q){l=1.70158;var s=0,r=o;if(k==0)return m;if((k/=q/2)==2)return m+o;s||(s=q*0.3*1.5);if(r<Math.abs(o)){r=o;l=s/4}else l=s/(2*Math.PI)*Math.asin(o/
r);if(k<1)return-0.5*r*Math.pow(2,10*(k-=1))*Math.sin((k*q-l)*2*Math.PI/s)+m;return r*Math.pow(2,-10*(k-=1))*Math.sin((k*q-l)*2*Math.PI/s)*0.5+o+m},easeInBack:function(l,k,m,o,q,s){if(s==d)s=1.70158;return o*(k/=q)*k*((s+1)*k-s)+m},easeOutBack:function(l,k,m,o,q,s){if(s==d)s=1.70158;return o*((k=k/q-1)*k*((s+1)*k+s)+1)+m},easeInOutBack:function(l,k,m,o,q,s){if(s==d)s=1.70158;if((k/=q/2)<1)return o/2*k*k*(((s*=1.525)+1)*k-s)+m;return o/2*((k-=2)*k*(((s*=1.525)+1)*k+s)+2)+m},easeInBounce:function(l,
k,m,o,q){return o-b.easing.easeOutBounce(l,q-k,0,o,q)+m},easeOutBounce:function(l,k,m,o,q){return(k/=q)<1/2.75?o*7.5625*k*k+m:k<2/2.75?o*(7.5625*(k-=1.5/2.75)*k+0.75)+m:k<2.5/2.75?o*(7.5625*(k-=2.25/2.75)*k+0.9375)+m:o*(7.5625*(k-=2.625/2.75)*k+0.984375)+m},easeInOutBounce:function(l,k,m,o,q){if(k<q/2)return b.easing.easeInBounce(l,k*2,0,o,q)*0.5+m;return b.easing.easeOutBounce(l,k*2-q,0,o,q)*0.5+o*0.5+m}})}(jQuery);
(function(b){b.effects.blind=function(d){return this.queue(function(){var e=b(this),g=["position","top","bottom","left","right"],f=b.effects.setMode(e,d.options.mode||"hide"),a=d.options.direction||"vertical";b.effects.save(e,g);e.show();var c=b.effects.createWrapper(e).css({overflow:"hidden"}),h=a=="vertical"?"height":"width";a=a=="vertical"?c.height():c.width();f=="show"&&c.css(h,0);var i={};i[h]=f=="show"?a:0;c.animate(i,d.duration,d.options.easing,function(){f=="hide"&&e.hide();b.effects.restore(e,
g);b.effects.removeWrapper(e);d.callback&&d.callback.apply(e[0],arguments);e.dequeue()})})}})(jQuery);
(function(b){b.effects.bounce=function(d){return this.queue(function(){var e=b(this),g=["position","top","bottom","left","right"],f=b.effects.setMode(e,d.options.mode||"effect"),a=d.options.direction||"up",c=d.options.distance||20,h=d.options.times||5,i=d.duration||250;/show|hide/.test(f)&&g.push("opacity");b.effects.save(e,g);e.show();b.effects.createWrapper(e);var j=a=="up"||a=="down"?"top":"left";a=a=="up"||a=="left"?"pos":"neg";c=d.options.distance||(j=="top"?e.outerHeight({margin:true})/3:e.outerWidth({margin:true})/
3);if(f=="show")e.css("opacity",0).css(j,a=="pos"?-c:c);if(f=="hide")c/=h*2;f!="hide"&&h--;if(f=="show"){var n={opacity:1};n[j]=(a=="pos"?"+=":"-=")+c;e.animate(n,i/2,d.options.easing);c/=2;h--}for(n=0;n<h;n++){var p={},l={};p[j]=(a=="pos"?"-=":"+=")+c;l[j]=(a=="pos"?"+=":"-=")+c;e.animate(p,i/2,d.options.easing).animate(l,i/2,d.options.easing);c=f=="hide"?c*2:c/2}if(f=="hide"){n={opacity:0};n[j]=(a=="pos"?"-=":"+=")+c;e.animate(n,i/2,d.options.easing,function(){e.hide();b.effects.restore(e,g);b.effects.removeWrapper(e);
d.callback&&d.callback.apply(this,arguments)})}else{p={};l={};p[j]=(a=="pos"?"-=":"+=")+c;l[j]=(a=="pos"?"+=":"-=")+c;e.animate(p,i/2,d.options.easing).animate(l,i/2,d.options.easing,function(){b.effects.restore(e,g);b.effects.removeWrapper(e);d.callback&&d.callback.apply(this,arguments)})}e.queue("fx",function(){e.dequeue()});e.dequeue()})}})(jQuery);
(function(b){b.effects.clip=function(d){return this.queue(function(){var e=b(this),g=["position","top","bottom","left","right","height","width"],f=b.effects.setMode(e,d.options.mode||"hide"),a=d.options.direction||"vertical";b.effects.save(e,g);e.show();var c=b.effects.createWrapper(e).css({overflow:"hidden"});c=e[0].tagName=="IMG"?c:e;var h={size:a=="vertical"?"height":"width",position:a=="vertical"?"top":"left"};a=a=="vertical"?c.height():c.width();if(f=="show"){c.css(h.size,0);c.css(h.position,
a/2)}var i={};i[h.size]=f=="show"?a:0;i[h.position]=f=="show"?0:a/2;c.animate(i,{queue:false,duration:d.duration,easing:d.options.easing,complete:function(){f=="hide"&&e.hide();b.effects.restore(e,g);b.effects.removeWrapper(e);d.callback&&d.callback.apply(e[0],arguments);e.dequeue()}})})}})(jQuery);
(function(b){b.effects.drop=function(d){return this.queue(function(){var e=b(this),g=["position","top","bottom","left","right","opacity"],f=b.effects.setMode(e,d.options.mode||"hide"),a=d.options.direction||"left";b.effects.save(e,g);e.show();b.effects.createWrapper(e);var c=a=="up"||a=="down"?"top":"left";a=a=="up"||a=="left"?"pos":"neg";var h=d.options.distance||(c=="top"?e.outerHeight({margin:true})/2:e.outerWidth({margin:true})/2);if(f=="show")e.css("opacity",0).css(c,a=="pos"?-h:h);var i={opacity:f==
"show"?1:0};i[c]=(f=="show"?a=="pos"?"+=":"-=":a=="pos"?"-=":"+=")+h;e.animate(i,{queue:false,duration:d.duration,easing:d.options.easing,complete:function(){f=="hide"&&e.hide();b.effects.restore(e,g);b.effects.removeWrapper(e);d.callback&&d.callback.apply(this,arguments);e.dequeue()}})})}})(jQuery);
(function(b){b.effects.explode=function(d){return this.queue(function(){var e=d.options.pieces?Math.round(Math.sqrt(d.options.pieces)):3,g=d.options.pieces?Math.round(Math.sqrt(d.options.pieces)):3;d.options.mode=d.options.mode=="toggle"?b(this).is(":visible")?"hide":"show":d.options.mode;var f=b(this).show().css("visibility","hidden"),a=f.offset();a.top-=parseInt(f.css("marginTop"),10)||0;a.left-=parseInt(f.css("marginLeft"),10)||0;for(var c=f.outerWidth(true),h=f.outerHeight(true),i=0;i<e;i++)for(var j=
0;j<g;j++)f.clone().appendTo("body").wrap("<div></div>").css({position:"absolute",visibility:"visible",left:-j*(c/g),top:-i*(h/e)}).parent().addClass("ui-effects-explode").css({position:"absolute",overflow:"hidden",width:c/g,height:h/e,left:a.left+j*(c/g)+(d.options.mode=="show"?(j-Math.floor(g/2))*(c/g):0),top:a.top+i*(h/e)+(d.options.mode=="show"?(i-Math.floor(e/2))*(h/e):0),opacity:d.options.mode=="show"?0:1}).animate({left:a.left+j*(c/g)+(d.options.mode=="show"?0:(j-Math.floor(g/2))*(c/g)),top:a.top+
i*(h/e)+(d.options.mode=="show"?0:(i-Math.floor(e/2))*(h/e)),opacity:d.options.mode=="show"?1:0},d.duration||500);setTimeout(function(){d.options.mode=="show"?f.css({visibility:"visible"}):f.css({visibility:"visible"}).hide();d.callback&&d.callback.apply(f[0]);f.dequeue();b("div.ui-effects-explode").remove()},d.duration||500)})}})(jQuery);
(function(b){b.effects.fade=function(d){return this.queue(function(){var e=b(this),g=b.effects.setMode(e,d.options.mode||"hide");e.animate({opacity:g},{queue:false,duration:d.duration,easing:d.options.easing,complete:function(){d.callback&&d.callback.apply(this,arguments);e.dequeue()}})})}})(jQuery);
(function(b){b.effects.fold=function(d){return this.queue(function(){var e=b(this),g=["position","top","bottom","left","right"],f=b.effects.setMode(e,d.options.mode||"hide"),a=d.options.size||15,c=!!d.options.horizFirst,h=d.duration?d.duration/2:b.fx.speeds._default/2;b.effects.save(e,g);e.show();var i=b.effects.createWrapper(e).css({overflow:"hidden"}),j=f=="show"!=c,n=j?["width","height"]:["height","width"];j=j?[i.width(),i.height()]:[i.height(),i.width()];var p=/([0-9]+)%/.exec(a);if(p)a=parseInt(p[1],
10)/100*j[f=="hide"?0:1];if(f=="show")i.css(c?{height:0,width:a}:{height:a,width:0});c={};p={};c[n[0]]=f=="show"?j[0]:a;p[n[1]]=f=="show"?j[1]:0;i.animate(c,h,d.options.easing).animate(p,h,d.options.easing,function(){f=="hide"&&e.hide();b.effects.restore(e,g);b.effects.removeWrapper(e);d.callback&&d.callback.apply(e[0],arguments);e.dequeue()})})}})(jQuery);
(function(b){b.effects.highlight=function(d){return this.queue(function(){var e=b(this),g=["backgroundImage","backgroundColor","opacity"],f=b.effects.setMode(e,d.options.mode||"show"),a={backgroundColor:e.css("backgroundColor")};if(f=="hide")a.opacity=0;b.effects.save(e,g);e.show().css({backgroundImage:"none",backgroundColor:d.options.color||"#ffff99"}).animate(a,{queue:false,duration:d.duration,easing:d.options.easing,complete:function(){f=="hide"&&e.hide();b.effects.restore(e,g);f=="show"&&!b.support.opacity&&
this.style.removeAttribute("filter");d.callback&&d.callback.apply(this,arguments);e.dequeue()}})})}})(jQuery);
(function(b){b.effects.pulsate=function(d){return this.queue(function(){var e=b(this),g=b.effects.setMode(e,d.options.mode||"show");times=(d.options.times||5)*2-1;duration=d.duration?d.duration/2:b.fx.speeds._default/2;isVisible=e.is(":visible");animateTo=0;if(!isVisible){e.css("opacity",0).show();animateTo=1}if(g=="hide"&&isVisible||g=="show"&&!isVisible)times--;for(g=0;g<times;g++){e.animate({opacity:animateTo},duration,d.options.easing);animateTo=(animateTo+1)%2}e.animate({opacity:animateTo},duration,
d.options.easing,function(){animateTo==0&&e.hide();d.callback&&d.callback.apply(this,arguments)});e.queue("fx",function(){e.dequeue()}).dequeue()})}})(jQuery);
(function(b){b.effects.puff=function(d){return this.queue(function(){var e=b(this),g=b.effects.setMode(e,d.options.mode||"hide"),f=parseInt(d.options.percent,10)||150,a=f/100,c={height:e.height(),width:e.width()};b.extend(d.options,{fade:true,mode:g,percent:g=="hide"?f:100,from:g=="hide"?c:{height:c.height*a,width:c.width*a}});e.effect("scale",d.options,d.duration,d.callback);e.dequeue()})};b.effects.scale=function(d){return this.queue(function(){var e=b(this),g=b.extend(true,{},d.options),f=b.effects.setMode(e,
d.options.mode||"effect"),a=parseInt(d.options.percent,10)||(parseInt(d.options.percent,10)==0?0:f=="hide"?0:100),c=d.options.direction||"both",h=d.options.origin;if(f!="effect"){g.origin=h||["middle","center"];g.restore=true}h={height:e.height(),width:e.width()};e.from=d.options.from||(f=="show"?{height:0,width:0}:h);a={y:c!="horizontal"?a/100:1,x:c!="vertical"?a/100:1};e.to={height:h.height*a.y,width:h.width*a.x};if(d.options.fade){if(f=="show"){e.from.opacity=0;e.to.opacity=1}if(f=="hide"){e.from.opacity=
1;e.to.opacity=0}}g.from=e.from;g.to=e.to;g.mode=f;e.effect("size",g,d.duration,d.callback);e.dequeue()})};b.effects.size=function(d){return this.queue(function(){var e=b(this),g=["position","top","bottom","left","right","width","height","overflow","opacity"],f=["position","top","bottom","left","right","overflow","opacity"],a=["width","height","overflow"],c=["fontSize"],h=["borderTopWidth","borderBottomWidth","paddingTop","paddingBottom"],i=["borderLeftWidth","borderRightWidth","paddingLeft","paddingRight"],
j=b.effects.setMode(e,d.options.mode||"effect"),n=d.options.restore||false,p=d.options.scale||"both",l=d.options.origin,k={height:e.height(),width:e.width()};e.from=d.options.from||k;e.to=d.options.to||k;if(l){l=b.effects.getBaseline(l,k);e.from.top=(k.height-e.from.height)*l.y;e.from.left=(k.width-e.from.width)*l.x;e.to.top=(k.height-e.to.height)*l.y;e.to.left=(k.width-e.to.width)*l.x}var m={from:{y:e.from.height/k.height,x:e.from.width/k.width},to:{y:e.to.height/k.height,x:e.to.width/k.width}};
if(p=="box"||p=="both"){if(m.from.y!=m.to.y){g=g.concat(h);e.from=b.effects.setTransition(e,h,m.from.y,e.from);e.to=b.effects.setTransition(e,h,m.to.y,e.to)}if(m.from.x!=m.to.x){g=g.concat(i);e.from=b.effects.setTransition(e,i,m.from.x,e.from);e.to=b.effects.setTransition(e,i,m.to.x,e.to)}}if(p=="content"||p=="both")if(m.from.y!=m.to.y){g=g.concat(c);e.from=b.effects.setTransition(e,c,m.from.y,e.from);e.to=b.effects.setTransition(e,c,m.to.y,e.to)}b.effects.save(e,n?g:f);e.show();b.effects.createWrapper(e);
e.css("overflow","hidden").css(e.from);if(p=="content"||p=="both"){h=h.concat(["marginTop","marginBottom"]).concat(c);i=i.concat(["marginLeft","marginRight"]);a=g.concat(h).concat(i);e.find("*[width]").each(function(){child=b(this);n&&b.effects.save(child,a);var o={height:child.height(),width:child.width()};child.from={height:o.height*m.from.y,width:o.width*m.from.x};child.to={height:o.height*m.to.y,width:o.width*m.to.x};if(m.from.y!=m.to.y){child.from=b.effects.setTransition(child,h,m.from.y,child.from);
child.to=b.effects.setTransition(child,h,m.to.y,child.to)}if(m.from.x!=m.to.x){child.from=b.effects.setTransition(child,i,m.from.x,child.from);child.to=b.effects.setTransition(child,i,m.to.x,child.to)}child.css(child.from);child.animate(child.to,d.duration,d.options.easing,function(){n&&b.effects.restore(child,a)})})}e.animate(e.to,{queue:false,duration:d.duration,easing:d.options.easing,complete:function(){e.to.opacity===0&&e.css("opacity",e.from.opacity);j=="hide"&&e.hide();b.effects.restore(e,
n?g:f);b.effects.removeWrapper(e);d.callback&&d.callback.apply(this,arguments);e.dequeue()}})})}})(jQuery);
(function(b){b.effects.shake=function(d){return this.queue(function(){var e=b(this),g=["position","top","bottom","left","right"];b.effects.setMode(e,d.options.mode||"effect");var f=d.options.direction||"left",a=d.options.distance||20,c=d.options.times||3,h=d.duration||d.options.duration||140;b.effects.save(e,g);e.show();b.effects.createWrapper(e);var i=f=="up"||f=="down"?"top":"left",j=f=="up"||f=="left"?"pos":"neg";f={};var n={},p={};f[i]=(j=="pos"?"-=":"+=")+a;n[i]=(j=="pos"?"+=":"-=")+a*2;p[i]=
(j=="pos"?"-=":"+=")+a*2;e.animate(f,h,d.options.easing);for(a=1;a<c;a++)e.animate(n,h,d.options.easing).animate(p,h,d.options.easing);e.animate(n,h,d.options.easing).animate(f,h/2,d.options.easing,function(){b.effects.restore(e,g);b.effects.removeWrapper(e);d.callback&&d.callback.apply(this,arguments)});e.queue("fx",function(){e.dequeue()});e.dequeue()})}})(jQuery);
(function(b){b.effects.slide=function(d){return this.queue(function(){var e=b(this),g=["position","top","bottom","left","right"],f=b.effects.setMode(e,d.options.mode||"show"),a=d.options.direction||"left";b.effects.save(e,g);e.show();b.effects.createWrapper(e).css({overflow:"hidden"});var c=a=="up"||a=="down"?"top":"left";a=a=="up"||a=="left"?"pos":"neg";var h=d.options.distance||(c=="top"?e.outerHeight({margin:true}):e.outerWidth({margin:true}));if(f=="show")e.css(c,a=="pos"?isNaN(h)?"-"+h:-h:h);
var i={};i[c]=(f=="show"?a=="pos"?"+=":"-=":a=="pos"?"-=":"+=")+h;e.animate(i,{queue:false,duration:d.duration,easing:d.options.easing,complete:function(){f=="hide"&&e.hide();b.effects.restore(e,g);b.effects.removeWrapper(e);d.callback&&d.callback.apply(this,arguments);e.dequeue()}})})}})(jQuery);
(function(b){b.effects.transfer=function(d){return this.queue(function(){var e=b(this),g=b(d.options.to),f=g.offset();g={top:f.top,left:f.left,height:g.innerHeight(),width:g.innerWidth()};f=e.offset();var a=b('<div class="ui-effects-transfer"></div>').appendTo(document.body).addClass(d.options.className).css({top:f.top,left:f.left,height:e.innerHeight(),width:e.innerWidth(),position:"absolute"}).animate(g,d.duration,d.options.easing,function(){a.remove();d.callback&&d.callback.apply(e[0],arguments);
e.dequeue()})})}})(jQuery);
(function(b){b.widget("ui.accordion",{options:{active:0,animated:"slide",autoHeight:true,clearStyle:false,collapsible:false,event:"click",fillSpace:false,header:"> li > :first-child,> :not(li):even",icons:{header:"ui-icon-triangle-1-e",headerSelected:"ui-icon-triangle-1-s"},navigation:false,navigationFilter:function(){return this.href.toLowerCase()===location.href.toLowerCase()}},_create:function(){var d=this,e=d.options;d.running=0;d.element.addClass("ui-accordion ui-widget ui-helper-reset").children("li").addClass("ui-accordion-li-fix");d.headers=
d.element.find(e.header).addClass("ui-accordion-header ui-helper-reset ui-state-default ui-corner-all").bind("mouseenter.accordion",function(){e.disabled||b(this).addClass("ui-state-hover")}).bind("mouseleave.accordion",function(){e.disabled||b(this).removeClass("ui-state-hover")}).bind("focus.accordion",function(){e.disabled||b(this).addClass("ui-state-focus")}).bind("blur.accordion",function(){e.disabled||b(this).removeClass("ui-state-focus")});d.headers.next().addClass("ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom");
if(e.navigation){var g=d.element.find("a").filter(e.navigationFilter).eq(0);if(g.length){var f=g.closest(".ui-accordion-header");d.active=f.length?f:g.closest(".ui-accordion-content").prev()}}d.active=d._findActive(d.active||e.active).addClass("ui-state-default ui-state-active").toggleClass("ui-corner-all").toggleClass("ui-corner-top");d.active.next().addClass("ui-accordion-content-active");d._createIcons();d.resize();d.element.attr("role","tablist");d.headers.attr("role","tab").bind("keydown.accordion",
function(a){return d._keydown(a)}).next().attr("role","tabpanel");d.headers.not(d.active||"").attr({"aria-expanded":"false","aria-selected":"false",tabIndex:-1}).next().hide();d.active.length?d.active.attr({"aria-expanded":"true","aria-selected":"true",tabIndex:0}):d.headers.eq(0).attr("tabIndex",0);b.browser.safari||d.headers.find("a").attr("tabIndex",-1);e.event&&d.headers.bind(e.event.split(" ").join(".accordion ")+".accordion",function(a){d._clickHandler.call(d,a,this);a.preventDefault()})},_createIcons:function(){var d=
this.options;if(d.icons){b("<span></span>").addClass("ui-icon "+d.icons.header).prependTo(this.headers);this.active.children(".ui-icon").toggleClass(d.icons.header).toggleClass(d.icons.headerSelected);this.element.addClass("ui-accordion-icons")}},_destroyIcons:function(){this.headers.children(".ui-icon").remove();this.element.removeClass("ui-accordion-icons")},destroy:function(){var d=this.options;this.element.removeClass("ui-accordion ui-widget ui-helper-reset").removeAttr("role");this.headers.unbind(".accordion").removeClass("ui-accordion-header ui-accordion-disabled ui-helper-reset ui-state-default ui-corner-all ui-state-active ui-state-disabled ui-corner-top").removeAttr("role").removeAttr("aria-expanded").removeAttr("aria-selected").removeAttr("tabIndex");
this.headers.find("a").removeAttr("tabIndex");this._destroyIcons();var e=this.headers.next().css("display","").removeAttr("role").removeClass("ui-helper-reset ui-widget-content ui-corner-bottom ui-accordion-content ui-accordion-content-active ui-accordion-disabled ui-state-disabled");if(d.autoHeight||d.fillHeight)e.css("height","");return b.Widget.prototype.destroy.call(this)},_setOption:function(d,e){b.Widget.prototype._setOption.apply(this,arguments);d=="active"&&this.activate(e);if(d=="icons"){this._destroyIcons();
e&&this._createIcons()}if(d=="disabled")this.headers.add(this.headers.next())[e?"addClass":"removeClass"]("ui-accordion-disabled ui-state-disabled")},_keydown:function(d){if(!(this.options.disabled||d.altKey||d.ctrlKey)){var e=b.ui.keyCode,g=this.headers.length,f=this.headers.index(d.target),a=false;switch(d.keyCode){case e.RIGHT:case e.DOWN:a=this.headers[(f+1)%g];break;case e.LEFT:case e.UP:a=this.headers[(f-1+g)%g];break;case e.SPACE:case e.ENTER:this._clickHandler({target:d.target},d.target);
d.preventDefault()}if(a){b(d.target).attr("tabIndex",-1);b(a).attr("tabIndex",0);a.focus();return false}return true}},resize:function(){var d=this.options,e;if(d.fillSpace){if(b.browser.msie){var g=this.element.parent().css("overflow");this.element.parent().css("overflow","hidden")}e=this.element.parent().height();b.browser.msie&&this.element.parent().css("overflow",g);this.headers.each(function(){e-=b(this).outerHeight(true)});this.headers.next().each(function(){b(this).height(Math.max(0,e-b(this).innerHeight()+
b(this).height()))}).css("overflow","auto")}else if(d.autoHeight){e=0;this.headers.next().each(function(){e=Math.max(e,b(this).height("").height())}).height(e)}return this},activate:function(d){this.options.active=d;d=this._findActive(d)[0];this._clickHandler({target:d},d);return this},_findActive:function(d){return d?typeof d==="number"?this.headers.filter(":eq("+d+")"):this.headers.not(this.headers.not(d)):d===false?b([]):this.headers.filter(":eq(0)")},_clickHandler:function(d,e){var g=this.options;
if(!g.disabled)if(d.target){d=b(d.currentTarget||e);e=d[0]===this.active[0];g.active=g.collapsible&&e?false:this.headers.index(d);if(!(this.running||!g.collapsible&&e)){var f=this.active;i=d.next();c=this.active.next();h={options:g,newHeader:e&&g.collapsible?b([]):d,oldHeader:this.active,newContent:e&&g.collapsible?b([]):i,oldContent:c};var a=this.headers.index(this.active[0])>this.headers.index(d[0]);this.active=e?b([]):d;this._toggle(i,c,h,e,a);f.removeClass("ui-state-active ui-corner-top").addClass("ui-state-default ui-corner-all").children(".ui-icon").removeClass(g.icons.headerSelected).addClass(g.icons.header);
if(!e){d.removeClass("ui-state-default ui-corner-all").addClass("ui-state-active ui-corner-top").children(".ui-icon").removeClass(g.icons.header).addClass(g.icons.headerSelected);d.next().addClass("ui-accordion-content-active")}}}else if(g.collapsible){this.active.removeClass("ui-state-active ui-corner-top").addClass("ui-state-default ui-corner-all").children(".ui-icon").removeClass(g.icons.headerSelected).addClass(g.icons.header);this.active.next().addClass("ui-accordion-content-active");var c=this.active.next(),
h={options:g,newHeader:b([]),oldHeader:g.active,newContent:b([]),oldContent:c},i=this.active=b([]);this._toggle(i,c,h)}},_toggle:function(d,e,g,f,a){var c=this,h=c.options;c.toShow=d;c.toHide=e;c.data=g;var i=function(){if(c)return c._completed.apply(c,arguments)};c._trigger("changestart",null,c.data);c.running=e.size()===0?d.size():e.size();if(h.animated){g={};g=h.collapsible&&f?{toShow:b([]),toHide:e,complete:i,down:a,autoHeight:h.autoHeight||h.fillSpace}:{toShow:d,toHide:e,complete:i,down:a,autoHeight:h.autoHeight||
h.fillSpace};if(!h.proxied)h.proxied=h.animated;if(!h.proxiedDuration)h.proxiedDuration=h.duration;h.animated=b.isFunction(h.proxied)?h.proxied(g):h.proxied;h.duration=b.isFunction(h.proxiedDuration)?h.proxiedDuration(g):h.proxiedDuration;f=b.ui.accordion.animations;var j=h.duration,n=h.animated;if(n&&!f[n]&&!b.easing[n])n="slide";f[n]||(f[n]=function(p){this.slide(p,{easing:n,duration:j||700})});f[n](g)}else{if(h.collapsible&&f)d.toggle();else{e.hide();d.show()}i(true)}e.prev().attr({"aria-expanded":"false",
"aria-selected":"false",tabIndex:-1}).blur();d.prev().attr({"aria-expanded":"true","aria-selected":"true",tabIndex:0}).focus()},_completed:function(d){this.running=d?0:--this.running;if(!this.running){this.options.clearStyle&&this.toShow.add(this.toHide).css({height:"",overflow:""});this.toHide.removeClass("ui-accordion-content-active");if(this.toHide.length)this.toHide.parent()[0].className=this.toHide.parent()[0].className;this._trigger("change",null,this.data)}}});b.extend(b.ui.accordion,{version:"1.8.11",
animations:{slide:function(d,e){d=b.extend({easing:"swing",duration:300},d,e);if(d.toHide.size())if(d.toShow.size()){var g=d.toShow.css("overflow"),f=0,a={},c={},h;e=d.toShow;h=e[0].style.width;e.width(parseInt(e.parent().width(),10)-parseInt(e.css("paddingLeft"),10)-parseInt(e.css("paddingRight"),10)-(parseInt(e.css("borderLeftWidth"),10)||0)-(parseInt(e.css("borderRightWidth"),10)||0));b.each(["height","paddingTop","paddingBottom"],function(i,j){c[j]="hide";i=(""+b.css(d.toShow[0],j)).match(/^([\d+-.]+)(.*)$/);
a[j]={value:i[1],unit:i[2]||"px"}});d.toShow.css({height:0,overflow:"hidden"}).show();d.toHide.filter(":hidden").each(d.complete).end().filter(":visible").animate(c,{step:function(i,j){if(j.prop=="height")f=j.end-j.start===0?0:(j.now-j.start)/(j.end-j.start);d.toShow[0].style[j.prop]=f*a[j.prop].value+a[j.prop].unit},duration:d.duration,easing:d.easing,complete:function(){d.autoHeight||d.toShow.css("height","");d.toShow.css({width:h,overflow:g});d.complete()}})}else d.toHide.animate({height:"hide",
paddingTop:"hide",paddingBottom:"hide"},d);else d.toShow.animate({height:"show",paddingTop:"show",paddingBottom:"show"},d)},bounceslide:function(d){this.slide(d,{easing:d.down?"easeOutBounce":"swing",duration:d.down?1E3:200})}}})})(jQuery);
(function(b){var d=0;b.widget("ui.autocomplete",{options:{appendTo:"body",autoFocus:false,delay:300,minLength:1,position:{my:"left top",at:"left bottom",collision:"none"},source:null},pending:0,_create:function(){var e=this,g=this.element[0].ownerDocument,f;this.element.addClass("ui-autocomplete-input").attr("autocomplete","off").attr({role:"textbox","aria-autocomplete":"list","aria-haspopup":"true"}).bind("keydown.autocomplete",function(a){if(!(e.options.disabled||e.element.attr("readonly"))){f=
false;var c=b.ui.keyCode;switch(a.keyCode){case c.PAGE_UP:e._move("previousPage",a);break;case c.PAGE_DOWN:e._move("nextPage",a);break;case c.UP:e._move("previous",a);a.preventDefault();break;case c.DOWN:e._move("next",a);a.preventDefault();break;case c.ENTER:case c.NUMPAD_ENTER:if(e.menu.active){f=true;a.preventDefault()}case c.TAB:if(!e.menu.active)return;e.menu.select(a);break;case c.ESCAPE:e.element.val(e.term);e.close(a);break;default:clearTimeout(e.searching);e.searching=setTimeout(function(){if(e.term!=
e.element.val()){e.selectedItem=null;e.search(null,a)}},e.options.delay);break}}}).bind("keypress.autocomplete",function(a){if(f){f=false;a.preventDefault()}}).bind("focus.autocomplete",function(){if(!e.options.disabled){e.selectedItem=null;e.previous=e.element.val()}}).bind("blur.autocomplete",function(a){if(!e.options.disabled){clearTimeout(e.searching);e.closing=setTimeout(function(){e.close(a);e._change(a)},150)}});this._initSource();this.response=function(){return e._response.apply(e,arguments)};
this.menu=b("<ul></ul>").addClass("ui-autocomplete").appendTo(b(this.options.appendTo||"body",g)[0]).mousedown(function(a){var c=e.menu.element[0];b(a.target).closest(".ui-menu-item").length||setTimeout(function(){b(document).one("mousedown",function(h){h.target!==e.element[0]&&h.target!==c&&!b.ui.contains(c,h.target)&&e.close()})},1);setTimeout(function(){clearTimeout(e.closing)},13)}).menu({focus:function(a,c){c=c.item.data("item.autocomplete");false!==e._trigger("focus",a,{item:c})&&/^key/.test(a.originalEvent.type)&&
e.element.val(c.value)},selected:function(a,c){var h=c.item.data("item.autocomplete"),i=e.previous;if(e.element[0]!==g.activeElement){e.element.focus();e.previous=i;setTimeout(function(){e.previous=i;e.selectedItem=h},1)}false!==e._trigger("select",a,{item:h})&&e.element.val(h.value);e.term=e.element.val();e.close(a);e.selectedItem=h},blur:function(){e.menu.element.is(":visible")&&e.element.val()!==e.term&&e.element.val(e.term)}}).zIndex(this.element.zIndex()+1).css({top:0,left:0}).hide().data("menu");
b.fn.bgiframe&&this.menu.element.bgiframe()},destroy:function(){this.element.removeClass("ui-autocomplete-input").removeAttr("autocomplete").removeAttr("role").removeAttr("aria-autocomplete").removeAttr("aria-haspopup");this.menu.element.remove();b.Widget.prototype.destroy.call(this)},_setOption:function(e,g){b.Widget.prototype._setOption.apply(this,arguments);e==="source"&&this._initSource();if(e==="appendTo")this.menu.element.appendTo(b(g||"body",this.element[0].ownerDocument)[0]);e==="disabled"&&
g&&this.xhr&&this.xhr.abort()},_initSource:function(){var e=this,g,f;if(b.isArray(this.options.source)){g=this.options.source;this.source=function(a,c){c(b.ui.autocomplete.filter(g,a.term))}}else if(typeof this.options.source==="string"){f=this.options.source;this.source=function(a,c){e.xhr&&e.xhr.abort();e.xhr=b.ajax({url:f,data:a,dataType:"json",autocompleteRequest:++d,success:function(h){this.autocompleteRequest===d&&c(h)},error:function(){this.autocompleteRequest===d&&c([])}})}}else this.source=
this.options.source},search:function(e,g){e=e!=null?e:this.element.val();this.term=this.element.val();if(e.length<this.options.minLength)return this.close(g);clearTimeout(this.closing);if(this._trigger("search",g)!==false)return this._search(e)},_search:function(e){this.pending++;this.element.addClass("ui-autocomplete-loading");this.source({term:e},this.response)},_response:function(e){if(!this.options.disabled&&e&&e.length){e=this._normalize(e);this._suggest(e);this._trigger("open")}else this.close();
this.pending--;this.pending||this.element.removeClass("ui-autocomplete-loading")},close:function(e){clearTimeout(this.closing);if(this.menu.element.is(":visible")){this.menu.element.hide();this.menu.deactivate();this._trigger("close",e)}},_change:function(e){this.previous!==this.element.val()&&this._trigger("change",e,{item:this.selectedItem})},_normalize:function(e){if(e.length&&e[0].label&&e[0].value)return e;return b.map(e,function(g){if(typeof g==="string")return{label:g,value:g};return b.extend({label:g.label||
g.value,value:g.value||g.label},g)})},_suggest:function(e){var g=this.menu.element.empty().zIndex(this.element.zIndex()+1);this._renderMenu(g,e);this.menu.deactivate();this.menu.refresh();g.show();this._resizeMenu();g.position(b.extend({of:this.element},this.options.position));this.options.autoFocus&&this.menu.next(new b.Event("mouseover"))},_resizeMenu:function(){var e=this.menu.element;e.outerWidth(Math.max(e.width("").outerWidth(),this.element.outerWidth()))},_renderMenu:function(e,g){var f=this;
b.each(g,function(a,c){f._renderItem(e,c)})},_renderItem:function(e,g){return b("<li></li>").data("item.autocomplete",g).append(b("<a></a>").text(g.label)).appendTo(e)},_move:function(e,g){if(this.menu.element.is(":visible"))if(this.menu.first()&&/^previous/.test(e)||this.menu.last()&&/^next/.test(e)){this.element.val(this.term);this.menu.deactivate()}else this.menu[e](g);else this.search(null,g)},widget:function(){return this.menu.element}});b.extend(b.ui.autocomplete,{escapeRegex:function(e){return e.replace(/[-[\]{}()*+?.,\\^$|#\s]/g,
"\\$&")},filter:function(e,g){var f=new RegExp(b.ui.autocomplete.escapeRegex(g),"i");return b.grep(e,function(a){return f.test(a.label||a.value||a)})}})})(jQuery);
(function(b){b.widget("ui.menu",{_create:function(){var d=this;this.element.addClass("ui-menu ui-widget ui-widget-content ui-corner-all").attr({role:"listbox","aria-activedescendant":"ui-active-menuitem"}).click(function(e){if(b(e.target).closest(".ui-menu-item a").length){e.preventDefault();d.select(e)}});this.refresh()},refresh:function(){var d=this;this.element.children("li:not(.ui-menu-item):has(a)").addClass("ui-menu-item").attr("role","menuitem").children("a").addClass("ui-corner-all").attr("tabindex",
-1).mouseenter(function(e){d.activate(e,b(this).parent())}).mouseleave(function(){d.deactivate()})},activate:function(d,e){this.deactivate();if(this.hasScroll()){var g=e.offset().top-this.element.offset().top,f=this.element.attr("scrollTop"),a=this.element.height();if(g<0)this.element.attr("scrollTop",f+g);else g>=a&&this.element.attr("scrollTop",f+g-a+e.height())}this.active=e.eq(0).children("a").addClass("ui-state-hover").attr("id","ui-active-menuitem").end();this._trigger("focus",d,{item:e})},
deactivate:function(){if(this.active){this.active.children("a").removeClass("ui-state-hover").removeAttr("id");this._trigger("blur");this.active=null}},next:function(d){this.move("next",".ui-menu-item:first",d)},previous:function(d){this.move("prev",".ui-menu-item:last",d)},first:function(){return this.active&&!this.active.prevAll(".ui-menu-item").length},last:function(){return this.active&&!this.active.nextAll(".ui-menu-item").length},move:function(d,e,g){if(this.active){d=this.active[d+"All"](".ui-menu-item").eq(0);
d.length?this.activate(g,d):this.activate(g,this.element.children(e))}else this.activate(g,this.element.children(e))},nextPage:function(d){if(this.hasScroll())if(!this.active||this.last())this.activate(d,this.element.children(".ui-menu-item:first"));else{var e=this.active.offset().top,g=this.element.height(),f=this.element.children(".ui-menu-item").filter(function(){var a=b(this).offset().top-e-g+b(this).height();return a<10&&a>-10});f.length||(f=this.element.children(".ui-menu-item:last"));this.activate(d,
f)}else this.activate(d,this.element.children(".ui-menu-item").filter(!this.active||this.last()?":first":":last"))},previousPage:function(d){if(this.hasScroll())if(!this.active||this.first())this.activate(d,this.element.children(".ui-menu-item:last"));else{var e=this.active.offset().top,g=this.element.height();result=this.element.children(".ui-menu-item").filter(function(){var f=b(this).offset().top-e+g-b(this).height();return f<10&&f>-10});result.length||(result=this.element.children(".ui-menu-item:first"));
this.activate(d,result)}else this.activate(d,this.element.children(".ui-menu-item").filter(!this.active||this.first()?":last":":first"))},hasScroll:function(){return this.element.height()<this.element.attr("scrollHeight")},select:function(d){this._trigger("selected",d,{item:this.active})}})})(jQuery);
(function(b){var d,e=function(f){b(":ui-button",f.target.form).each(function(){var a=b(this).data("button");setTimeout(function(){a.refresh()},1)})},g=function(f){var a=f.name,c=f.form,h=b([]);if(a)h=c?b(c).find("[name='"+a+"']"):b("[name='"+a+"']",f.ownerDocument).filter(function(){return!this.form});return h};b.widget("ui.button",{options:{disabled:null,text:true,label:null,icons:{primary:null,secondary:null}},_create:function(){this.element.closest("form").unbind("reset.button").bind("reset.button",
e);if(typeof this.options.disabled!=="boolean")this.options.disabled=this.element.attr("disabled");this._determineButtonType();this.hasTitle=!!this.buttonElement.attr("title");var f=this,a=this.options,c=this.type==="checkbox"||this.type==="radio",h="ui-state-hover"+(!c?" ui-state-active":"");if(a.label===null)a.label=this.buttonElement.html();if(this.element.is(":disabled"))a.disabled=true;this.buttonElement.addClass("ui-button ui-widget ui-state-default ui-corner-all").attr("role","button").bind("mouseenter.button",
function(){if(!a.disabled){b(this).addClass("ui-state-hover");this===d&&b(this).addClass("ui-state-active")}}).bind("mouseleave.button",function(){a.disabled||b(this).removeClass(h)}).bind("focus.button",function(){b(this).addClass("ui-state-focus")}).bind("blur.button",function(){b(this).removeClass("ui-state-focus")});c&&this.element.bind("change.button",function(){f.refresh()});if(this.type==="checkbox")this.buttonElement.bind("click.button",function(){if(a.disabled)return false;b(this).toggleClass("ui-state-active");
f.buttonElement.attr("aria-pressed",f.element[0].checked)});else if(this.type==="radio")this.buttonElement.bind("click.button",function(){if(a.disabled)return false;b(this).addClass("ui-state-active");f.buttonElement.attr("aria-pressed",true);var i=f.element[0];g(i).not(i).map(function(){return b(this).button("widget")[0]}).removeClass("ui-state-active").attr("aria-pressed",false)});else{this.buttonElement.bind("mousedown.button",function(){if(a.disabled)return false;b(this).addClass("ui-state-active");
d=this;b(document).one("mouseup",function(){d=null})}).bind("mouseup.button",function(){if(a.disabled)return false;b(this).removeClass("ui-state-active")}).bind("keydown.button",function(i){if(a.disabled)return false;if(i.keyCode==b.ui.keyCode.SPACE||i.keyCode==b.ui.keyCode.ENTER)b(this).addClass("ui-state-active")}).bind("keyup.button",function(){b(this).removeClass("ui-state-active")});this.buttonElement.is("a")&&this.buttonElement.keyup(function(i){i.keyCode===b.ui.keyCode.SPACE&&b(this).click()})}this._setOption("disabled",
a.disabled)},_determineButtonType:function(){this.type=this.element.is(":checkbox")?"checkbox":this.element.is(":radio")?"radio":this.element.is("input")?"input":"button";if(this.type==="checkbox"||this.type==="radio"){var f=this.element.parents().filter(":last"),a="label[for="+this.element.attr("id")+"]";this.buttonElement=f.find(a);if(!this.buttonElement.length){f=f.length?f.siblings():this.element.siblings();this.buttonElement=f.filter(a);if(!this.buttonElement.length)this.buttonElement=f.find(a)}this.element.addClass("ui-helper-hidden-accessible");
(f=this.element.is(":checked"))&&this.buttonElement.addClass("ui-state-active");this.buttonElement.attr("aria-pressed",f)}else this.buttonElement=this.element},widget:function(){return this.buttonElement},destroy:function(){this.element.removeClass("ui-helper-hidden-accessible");this.buttonElement.removeClass("ui-button ui-widget ui-state-default ui-corner-all ui-state-hover ui-state-active  ui-button-icons-only ui-button-icon-only ui-button-text-icons ui-button-text-icon-primary ui-button-text-icon-secondary ui-button-text-only").removeAttr("role").removeAttr("aria-pressed").html(this.buttonElement.find(".ui-button-text").html());
this.hasTitle||this.buttonElement.removeAttr("title");b.Widget.prototype.destroy.call(this)},_setOption:function(f,a){b.Widget.prototype._setOption.apply(this,arguments);if(f==="disabled")a?this.element.attr("disabled",true):this.element.removeAttr("disabled");this._resetButton()},refresh:function(){var f=this.element.is(":disabled");f!==this.options.disabled&&this._setOption("disabled",f);if(this.type==="radio")g(this.element[0]).each(function(){b(this).is(":checked")?b(this).button("widget").addClass("ui-state-active").attr("aria-pressed",
true):b(this).button("widget").removeClass("ui-state-active").attr("aria-pressed",false)});else if(this.type==="checkbox")this.element.is(":checked")?this.buttonElement.addClass("ui-state-active").attr("aria-pressed",true):this.buttonElement.removeClass("ui-state-active").attr("aria-pressed",false)},_resetButton:function(){if(this.type==="input")this.options.label&&this.element.val(this.options.label);else{var f=this.buttonElement.removeClass("ui-button-icons-only ui-button-icon-only ui-button-text-icons ui-button-text-icon-primary ui-button-text-icon-secondary ui-button-text-only"),
a=b("<span></span>").addClass("ui-button-text").html(this.options.label).appendTo(f.empty()).text(),c=this.options.icons,h=c.primary&&c.secondary,i=[];if(c.primary||c.secondary){if(this.options.text)i.push("ui-button-text-icon"+(h?"s":c.primary?"-primary":"-secondary"));c.primary&&f.prepend("<span class='ui-button-icon-primary ui-icon "+c.primary+"'></span>");c.secondary&&f.append("<span class='ui-button-icon-secondary ui-icon "+c.secondary+"'></span>");if(!this.options.text){i.push(h?"ui-button-icons-only":
"ui-button-icon-only");this.hasTitle||f.attr("title",a)}}else i.push("ui-button-text-only");f.addClass(i.join(" "))}}});b.widget("ui.buttonset",{options:{items:":button, :submit, :reset, :checkbox, :radio, a, :data(button)"},_create:function(){this.element.addClass("ui-buttonset")},_init:function(){this.refresh()},_setOption:function(f,a){f==="disabled"&&this.buttons.button("option",f,a);b.Widget.prototype._setOption.apply(this,arguments)},refresh:function(){this.buttons=this.element.find(this.options.items).filter(":ui-button").button("refresh").end().not(":ui-button").button().end().map(function(){return b(this).button("widget")[0]}).removeClass("ui-corner-all ui-corner-left ui-corner-right").filter(":first").addClass("ui-corner-left").end().filter(":last").addClass("ui-corner-right").end().end()},
destroy:function(){this.element.removeClass("ui-buttonset");this.buttons.map(function(){return b(this).button("widget")[0]}).removeClass("ui-corner-left ui-corner-right").end().button("destroy");b.Widget.prototype.destroy.call(this)}})})(jQuery);
(function(b,d){function e(){this.debug=false;this._curInst=null;this._keyEvent=false;this._disabledInputs=[];this._inDialog=this._datepickerShowing=false;this._mainDivId="ui-datepicker-div";this._inlineClass="ui-datepicker-inline";this._appendClass="ui-datepicker-append";this._triggerClass="ui-datepicker-trigger";this._dialogClass="ui-datepicker-dialog";this._disableClass="ui-datepicker-disabled";this._unselectableClass="ui-datepicker-unselectable";this._currentClass="ui-datepicker-current-day";this._dayOverClass=
"ui-datepicker-days-cell-over";this.regional=[];this.regional[""]={closeText:"Done",prevText:"Prev",nextText:"Next",currentText:"Today",monthNames:["January","February","March","April","May","June","July","August","September","October","November","December"],monthNamesShort:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],dayNames:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],dayNamesShort:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],dayNamesMin:["Su",
"Mo","Tu","We","Th","Fr","Sa"],weekHeader:"Wk",dateFormat:"mm/dd/yy",firstDay:0,isRTL:false,showMonthAfterYear:false,yearSuffix:""};this._defaults={showOn:"focus",showAnim:"fadeIn",showOptions:{},defaultDate:null,appendText:"",buttonText:"...",buttonImage:"",buttonImageOnly:false,hideIfNoPrevNext:false,navigationAsDateFormat:false,gotoCurrent:false,changeMonth:false,changeYear:false,yearRange:"c-10:c+10",showOtherMonths:false,selectOtherMonths:false,showWeek:false,calculateWeek:this.iso8601Week,shortYearCutoff:"+10",
minDate:null,maxDate:null,duration:"fast",beforeShowDay:null,beforeShow:null,onSelect:null,onChangeMonthYear:null,onClose:null,numberOfMonths:1,showCurrentAtPos:0,stepMonths:1,stepBigMonths:12,altField:"",altFormat:"",constrainInput:true,showButtonPanel:false,autoSize:false};b.extend(this._defaults,this.regional[""]);this.dpDiv=b('<div id="'+this._mainDivId+'" class="ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all"></div>')}function g(a,c){b.extend(a,c);for(var h in c)if(c[h]==
null||c[h]==d)a[h]=c[h];return a}b.extend(b.ui,{datepicker:{version:"1.8.11"}});var f=(new Date).getTime();b.extend(e.prototype,{markerClassName:"hasDatepicker",log:function(){this.debug&&console.log.apply("",arguments)},_widgetDatepicker:function(){return this.dpDiv},setDefaults:function(a){g(this._defaults,a||{});return this},_attachDatepicker:function(a,c){var h=null;for(var i in this._defaults){var j=a.getAttribute("date:"+i);if(j){h=h||{};try{h[i]=eval(j)}catch(n){h[i]=j}}}i=a.nodeName.toLowerCase();
j=i=="div"||i=="span";if(!a.id){this.uuid+=1;a.id="dp"+this.uuid}var p=this._newInst(b(a),j);p.settings=b.extend({},c||{},h||{});if(i=="input")this._connectDatepicker(a,p);else j&&this._inlineDatepicker(a,p)},_newInst:function(a,c){return{id:a[0].id.replace(/([^A-Za-z0-9_-])/g,"\\\\$1"),input:a,selectedDay:0,selectedMonth:0,selectedYear:0,drawMonth:0,drawYear:0,inline:c,dpDiv:!c?this.dpDiv:b('<div class="'+this._inlineClass+' ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all"></div>')}},
_connectDatepicker:function(a,c){var h=b(a);c.append=b([]);c.trigger=b([]);if(!h.hasClass(this.markerClassName)){this._attachments(h,c);h.addClass(this.markerClassName).keydown(this._doKeyDown).keypress(this._doKeyPress).keyup(this._doKeyUp).bind("setData.datepicker",function(i,j,n){c.settings[j]=n}).bind("getData.datepicker",function(i,j){return this._get(c,j)});this._autoSize(c);b.data(a,"datepicker",c)}},_attachments:function(a,c){var h=this._get(c,"appendText"),i=this._get(c,"isRTL");c.append&&
c.append.remove();if(h){c.append=b('<span class="'+this._appendClass+'">'+h+"</span>");a[i?"before":"after"](c.append)}a.unbind("focus",this._showDatepicker);c.trigger&&c.trigger.remove();h=this._get(c,"showOn");if(h=="focus"||h=="both")a.focus(this._showDatepicker);if(h=="button"||h=="both"){h=this._get(c,"buttonText");var j=this._get(c,"buttonImage");c.trigger=b(this._get(c,"buttonImageOnly")?b("<img/>").addClass(this._triggerClass).attr({src:j,alt:h,title:h}):b('<button type="button"></button>').addClass(this._triggerClass).html(j==
""?h:b("<img/>").attr({src:j,alt:h,title:h})));a[i?"before":"after"](c.trigger);c.trigger.click(function(){b.datepicker._datepickerShowing&&b.datepicker._lastInput==a[0]?b.datepicker._hideDatepicker():b.datepicker._showDatepicker(a[0]);return false})}},_autoSize:function(a){if(this._get(a,"autoSize")&&!a.inline){var c=new Date(2009,11,20),h=this._get(a,"dateFormat");if(h.match(/[DM]/)){var i=function(j){for(var n=0,p=0,l=0;l<j.length;l++)if(j[l].length>n){n=j[l].length;p=l}return p};c.setMonth(i(this._get(a,
h.match(/MM/)?"monthNames":"monthNamesShort")));c.setDate(i(this._get(a,h.match(/DD/)?"dayNames":"dayNamesShort"))+20-c.getDay())}a.input.attr("size",this._formatDate(a,c).length)}},_inlineDatepicker:function(a,c){var h=b(a);if(!h.hasClass(this.markerClassName)){h.addClass(this.markerClassName).append(c.dpDiv).bind("setData.datepicker",function(i,j,n){c.settings[j]=n}).bind("getData.datepicker",function(i,j){return this._get(c,j)});b.data(a,"datepicker",c);this._setDate(c,this._getDefaultDate(c),
true);this._updateDatepicker(c);this._updateAlternate(c);c.dpDiv.show()}},_dialogDatepicker:function(a,c,h,i,j){a=this._dialogInst;if(!a){this.uuid+=1;this._dialogInput=b('<input type="text" id="'+("dp"+this.uuid)+'" style="position: absolute; top: -100px; width: 0px; z-index: -10;"/>');this._dialogInput.keydown(this._doKeyDown);b("body").append(this._dialogInput);a=this._dialogInst=this._newInst(this._dialogInput,false);a.settings={};b.data(this._dialogInput[0],"datepicker",a)}g(a.settings,i||{});
c=c&&c.constructor==Date?this._formatDate(a,c):c;this._dialogInput.val(c);this._pos=j?j.length?j:[j.pageX,j.pageY]:null;if(!this._pos)this._pos=[document.documentElement.clientWidth/2-100+(document.documentElement.scrollLeft||document.body.scrollLeft),document.documentElement.clientHeight/2-150+(document.documentElement.scrollTop||document.body.scrollTop)];this._dialogInput.css("left",this._pos[0]+20+"px").css("top",this._pos[1]+"px");a.settings.onSelect=h;this._inDialog=true;this.dpDiv.addClass(this._dialogClass);
this._showDatepicker(this._dialogInput[0]);b.blockUI&&b.blockUI(this.dpDiv);b.data(this._dialogInput[0],"datepicker",a);return this},_destroyDatepicker:function(a){var c=b(a),h=b.data(a,"datepicker");if(c.hasClass(this.markerClassName)){var i=a.nodeName.toLowerCase();b.removeData(a,"datepicker");if(i=="input"){h.append.remove();h.trigger.remove();c.removeClass(this.markerClassName).unbind("focus",this._showDatepicker).unbind("keydown",this._doKeyDown).unbind("keypress",this._doKeyPress).unbind("keyup",
this._doKeyUp)}else if(i=="div"||i=="span")c.removeClass(this.markerClassName).empty()}},_enableDatepicker:function(a){var c=b(a),h=b.data(a,"datepicker");if(c.hasClass(this.markerClassName)){var i=a.nodeName.toLowerCase();if(i=="input"){a.disabled=false;h.trigger.filter("button").each(function(){this.disabled=false}).end().filter("img").css({opacity:"1.0",cursor:""})}else if(i=="div"||i=="span")c.children("."+this._inlineClass).children().removeClass("ui-state-disabled");this._disabledInputs=b.map(this._disabledInputs,
function(j){return j==a?null:j})}},_disableDatepicker:function(a){var c=b(a),h=b.data(a,"datepicker");if(c.hasClass(this.markerClassName)){var i=a.nodeName.toLowerCase();if(i=="input"){a.disabled=true;h.trigger.filter("button").each(function(){this.disabled=true}).end().filter("img").css({opacity:"0.5",cursor:"default"})}else if(i=="div"||i=="span")c.children("."+this._inlineClass).children().addClass("ui-state-disabled");this._disabledInputs=b.map(this._disabledInputs,function(j){return j==a?null:
j});this._disabledInputs[this._disabledInputs.length]=a}},_isDisabledDatepicker:function(a){if(!a)return false;for(var c=0;c<this._disabledInputs.length;c++)if(this._disabledInputs[c]==a)return true;return false},_getInst:function(a){try{return b.data(a,"datepicker")}catch(c){throw"Missing instance data for this datepicker";}},_optionDatepicker:function(a,c,h){var i=this._getInst(a);if(arguments.length==2&&typeof c=="string")return c=="defaults"?b.extend({},b.datepicker._defaults):i?c=="all"?b.extend({},
i.settings):this._get(i,c):null;var j=c||{};if(typeof c=="string"){j={};j[c]=h}if(i){this._curInst==i&&this._hideDatepicker();var n=this._getDateDatepicker(a,true),p=this._getMinMaxDate(i,"min"),l=this._getMinMaxDate(i,"max");g(i.settings,j);if(p!==null&&j.dateFormat!==d&&j.minDate===d)i.settings.minDate=this._formatDate(i,p);if(l!==null&&j.dateFormat!==d&&j.maxDate===d)i.settings.maxDate=this._formatDate(i,l);this._attachments(b(a),i);this._autoSize(i);this._setDateDatepicker(a,n);this._updateDatepicker(i)}},
_changeDatepicker:function(a,c,h){this._optionDatepicker(a,c,h)},_refreshDatepicker:function(a){(a=this._getInst(a))&&this._updateDatepicker(a)},_setDateDatepicker:function(a,c){if(a=this._getInst(a)){this._setDate(a,c);this._updateDatepicker(a);this._updateAlternate(a)}},_getDateDatepicker:function(a,c){(a=this._getInst(a))&&!a.inline&&this._setDateFromField(a,c);return a?this._getDate(a):null},_doKeyDown:function(a){var c=b.datepicker._getInst(a.target),h=true,i=c.dpDiv.is(".ui-datepicker-rtl");
c._keyEvent=true;if(b.datepicker._datepickerShowing)switch(a.keyCode){case 9:b.datepicker._hideDatepicker();h=false;break;case 13:h=b("td."+b.datepicker._dayOverClass+":not(."+b.datepicker._currentClass+")",c.dpDiv);h[0]?b.datepicker._selectDay(a.target,c.selectedMonth,c.selectedYear,h[0]):b.datepicker._hideDatepicker();return false;case 27:b.datepicker._hideDatepicker();break;case 33:b.datepicker._adjustDate(a.target,a.ctrlKey?-b.datepicker._get(c,"stepBigMonths"):-b.datepicker._get(c,"stepMonths"),
"M");break;case 34:b.datepicker._adjustDate(a.target,a.ctrlKey?+b.datepicker._get(c,"stepBigMonths"):+b.datepicker._get(c,"stepMonths"),"M");break;case 35:if(a.ctrlKey||a.metaKey)b.datepicker._clearDate(a.target);h=a.ctrlKey||a.metaKey;break;case 36:if(a.ctrlKey||a.metaKey)b.datepicker._gotoToday(a.target);h=a.ctrlKey||a.metaKey;break;case 37:if(a.ctrlKey||a.metaKey)b.datepicker._adjustDate(a.target,i?+1:-1,"D");h=a.ctrlKey||a.metaKey;if(a.originalEvent.altKey)b.datepicker._adjustDate(a.target,a.ctrlKey?
-b.datepicker._get(c,"stepBigMonths"):-b.datepicker._get(c,"stepMonths"),"M");break;case 38:if(a.ctrlKey||a.metaKey)b.datepicker._adjustDate(a.target,-7,"D");h=a.ctrlKey||a.metaKey;break;case 39:if(a.ctrlKey||a.metaKey)b.datepicker._adjustDate(a.target,i?-1:+1,"D");h=a.ctrlKey||a.metaKey;if(a.originalEvent.altKey)b.datepicker._adjustDate(a.target,a.ctrlKey?+b.datepicker._get(c,"stepBigMonths"):+b.datepicker._get(c,"stepMonths"),"M");break;case 40:if(a.ctrlKey||a.metaKey)b.datepicker._adjustDate(a.target,
+7,"D");h=a.ctrlKey||a.metaKey;break;default:h=false}else if(a.keyCode==36&&a.ctrlKey)b.datepicker._showDatepicker(this);else h=false;if(h){a.preventDefault();a.stopPropagation()}},_doKeyPress:function(a){var c=b.datepicker._getInst(a.target);if(b.datepicker._get(c,"constrainInput")){c=b.datepicker._possibleChars(b.datepicker._get(c,"dateFormat"));var h=String.fromCharCode(a.charCode==d?a.keyCode:a.charCode);return a.ctrlKey||a.metaKey||h<" "||!c||c.indexOf(h)>-1}},_doKeyUp:function(a){a=b.datepicker._getInst(a.target);
if(a.input.val()!=a.lastVal)try{if(b.datepicker.parseDate(b.datepicker._get(a,"dateFormat"),a.input?a.input.val():null,b.datepicker._getFormatConfig(a))){b.datepicker._setDateFromField(a);b.datepicker._updateAlternate(a);b.datepicker._updateDatepicker(a)}}catch(c){b.datepicker.log(c)}return true},_showDatepicker:function(a){a=a.target||a;if(a.nodeName.toLowerCase()!="input")a=b("input",a.parentNode)[0];if(!(b.datepicker._isDisabledDatepicker(a)||b.datepicker._lastInput==a)){var c=b.datepicker._getInst(a);
b.datepicker._curInst&&b.datepicker._curInst!=c&&b.datepicker._curInst.dpDiv.stop(true,true);var h=b.datepicker._get(c,"beforeShow");g(c.settings,h?h.apply(a,[a,c]):{});c.lastVal=null;b.datepicker._lastInput=a;b.datepicker._setDateFromField(c);if(b.datepicker._inDialog)a.value="";if(!b.datepicker._pos){b.datepicker._pos=b.datepicker._findPos(a);b.datepicker._pos[1]+=a.offsetHeight}var i=false;b(a).parents().each(function(){i|=b(this).css("position")=="fixed";return!i});if(i&&b.browser.opera){b.datepicker._pos[0]-=
document.documentElement.scrollLeft;b.datepicker._pos[1]-=document.documentElement.scrollTop}h={left:b.datepicker._pos[0],top:b.datepicker._pos[1]};b.datepicker._pos=null;c.dpDiv.empty();c.dpDiv.css({position:"absolute",display:"block",top:"-1000px"});b.datepicker._updateDatepicker(c);h=b.datepicker._checkOffset(c,h,i);c.dpDiv.css({position:b.datepicker._inDialog&&b.blockUI?"static":i?"fixed":"absolute",display:"none",left:h.left+"px",top:h.top+"px"});if(!c.inline){h=b.datepicker._get(c,"showAnim");
var j=b.datepicker._get(c,"duration"),n=function(){b.datepicker._datepickerShowing=true;var p=c.dpDiv.find("iframe.ui-datepicker-cover");if(p.length){var l=b.datepicker._getBorders(c.dpDiv);p.css({left:-l[0],top:-l[1],width:c.dpDiv.outerWidth(),height:c.dpDiv.outerHeight()})}};c.dpDiv.zIndex(b(a).zIndex()+1);b.effects&&b.effects[h]?c.dpDiv.show(h,b.datepicker._get(c,"showOptions"),j,n):c.dpDiv[h||"show"](h?j:null,n);if(!h||!j)n();c.input.is(":visible")&&!c.input.is(":disabled")&&c.input.focus();b.datepicker._curInst=
c}}},_updateDatepicker:function(a){var c=this,h=b.datepicker._getBorders(a.dpDiv);a.dpDiv.empty().append(this._generateHTML(a));var i=a.dpDiv.find("iframe.ui-datepicker-cover");i.length&&i.css({left:-h[0],top:-h[1],width:a.dpDiv.outerWidth(),height:a.dpDiv.outerHeight()});a.dpDiv.find("button, .ui-datepicker-prev, .ui-datepicker-next, .ui-datepicker-calendar td a").bind("mouseout",function(){b(this).removeClass("ui-state-hover");this.className.indexOf("ui-datepicker-prev")!=-1&&b(this).removeClass("ui-datepicker-prev-hover");
this.className.indexOf("ui-datepicker-next")!=-1&&b(this).removeClass("ui-datepicker-next-hover")}).bind("mouseover",function(){if(!c._isDisabledDatepicker(a.inline?a.dpDiv.parent()[0]:a.input[0])){b(this).parents(".ui-datepicker-calendar").find("a").removeClass("ui-state-hover");b(this).addClass("ui-state-hover");this.className.indexOf("ui-datepicker-prev")!=-1&&b(this).addClass("ui-datepicker-prev-hover");this.className.indexOf("ui-datepicker-next")!=-1&&b(this).addClass("ui-datepicker-next-hover")}}).end().find("."+
this._dayOverClass+" a").trigger("mouseover").end();h=this._getNumberOfMonths(a);i=h[1];i>1?a.dpDiv.addClass("ui-datepicker-multi-"+i).css("width",17*i+"em"):a.dpDiv.removeClass("ui-datepicker-multi-2 ui-datepicker-multi-3 ui-datepicker-multi-4").width("");a.dpDiv[(h[0]!=1||h[1]!=1?"add":"remove")+"Class"]("ui-datepicker-multi");a.dpDiv[(this._get(a,"isRTL")?"add":"remove")+"Class"]("ui-datepicker-rtl");a==b.datepicker._curInst&&b.datepicker._datepickerShowing&&a.input&&a.input.is(":visible")&&!a.input.is(":disabled")&&
a.input[0]!=document.activeElement&&a.input.focus();if(a.yearshtml){var j=a.yearshtml;setTimeout(function(){j===a.yearshtml&&a.dpDiv.find("select.ui-datepicker-year:first").replaceWith(a.yearshtml);j=a.yearshtml=null},0)}},_getBorders:function(a){var c=function(h){return{thin:1,medium:2,thick:3}[h]||h};return[parseFloat(c(a.css("border-left-width"))),parseFloat(c(a.css("border-top-width")))]},_checkOffset:function(a,c,h){var i=a.dpDiv.outerWidth(),j=a.dpDiv.outerHeight(),n=a.input?a.input.outerWidth():
0,p=a.input?a.input.outerHeight():0,l=document.documentElement.clientWidth+b(document).scrollLeft(),k=document.documentElement.clientHeight+b(document).scrollTop();c.left-=this._get(a,"isRTL")?i-n:0;c.left-=h&&c.left==a.input.offset().left?b(document).scrollLeft():0;c.top-=h&&c.top==a.input.offset().top+p?b(document).scrollTop():0;c.left-=Math.min(c.left,c.left+i>l&&l>i?Math.abs(c.left+i-l):0);c.top-=Math.min(c.top,c.top+j>k&&k>j?Math.abs(j+p):0);return c},_findPos:function(a){for(var c=this._get(this._getInst(a),
"isRTL");a&&(a.type=="hidden"||a.nodeType!=1||b.expr.filters.hidden(a));)a=a[c?"previousSibling":"nextSibling"];a=b(a).offset();return[a.left,a.top]},_hideDatepicker:function(a){var c=this._curInst;if(!(!c||a&&c!=b.data(a,"datepicker")))if(this._datepickerShowing){a=this._get(c,"showAnim");var h=this._get(c,"duration"),i=function(){b.datepicker._tidyDialog(c);this._curInst=null};b.effects&&b.effects[a]?c.dpDiv.hide(a,b.datepicker._get(c,"showOptions"),h,i):c.dpDiv[a=="slideDown"?"slideUp":a=="fadeIn"?
"fadeOut":"hide"](a?h:null,i);a||i();if(a=this._get(c,"onClose"))a.apply(c.input?c.input[0]:null,[c.input?c.input.val():"",c]);this._datepickerShowing=false;this._lastInput=null;if(this._inDialog){this._dialogInput.css({position:"absolute",left:"0",top:"-100px"});if(b.blockUI){b.unblockUI();b("body").append(this.dpDiv)}}this._inDialog=false}},_tidyDialog:function(a){a.dpDiv.removeClass(this._dialogClass).unbind(".ui-datepicker-calendar")},_checkExternalClick:function(a){if(b.datepicker._curInst){a=
b(a.target);a[0].id!=b.datepicker._mainDivId&&a.parents("#"+b.datepicker._mainDivId).length==0&&!a.hasClass(b.datepicker.markerClassName)&&!a.hasClass(b.datepicker._triggerClass)&&b.datepicker._datepickerShowing&&!(b.datepicker._inDialog&&b.blockUI)&&b.datepicker._hideDatepicker()}},_adjustDate:function(a,c,h){a=b(a);var i=this._getInst(a[0]);if(!this._isDisabledDatepicker(a[0])){this._adjustInstDate(i,c+(h=="M"?this._get(i,"showCurrentAtPos"):0),h);this._updateDatepicker(i)}},_gotoToday:function(a){a=
b(a);var c=this._getInst(a[0]);if(this._get(c,"gotoCurrent")&&c.currentDay){c.selectedDay=c.currentDay;c.drawMonth=c.selectedMonth=c.currentMonth;c.drawYear=c.selectedYear=c.currentYear}else{var h=new Date;c.selectedDay=h.getDate();c.drawMonth=c.selectedMonth=h.getMonth();c.drawYear=c.selectedYear=h.getFullYear()}this._notifyChange(c);this._adjustDate(a)},_selectMonthYear:function(a,c,h){a=b(a);var i=this._getInst(a[0]);i._selectingMonthYear=false;i["selected"+(h=="M"?"Month":"Year")]=i["draw"+(h==
"M"?"Month":"Year")]=parseInt(c.options[c.selectedIndex].value,10);this._notifyChange(i);this._adjustDate(a)},_clickMonthYear:function(a){var c=this._getInst(b(a)[0]);c.input&&c._selectingMonthYear&&setTimeout(function(){c.input.focus()},0);c._selectingMonthYear=!c._selectingMonthYear},_selectDay:function(a,c,h,i){var j=b(a);if(!(b(i).hasClass(this._unselectableClass)||this._isDisabledDatepicker(j[0]))){j=this._getInst(j[0]);j.selectedDay=j.currentDay=b("a",i).html();j.selectedMonth=j.currentMonth=
c;j.selectedYear=j.currentYear=h;this._selectDate(a,this._formatDate(j,j.currentDay,j.currentMonth,j.currentYear))}},_clearDate:function(a){a=b(a);this._getInst(a[0]);this._selectDate(a,"")},_selectDate:function(a,c){a=this._getInst(b(a)[0]);c=c!=null?c:this._formatDate(a);a.input&&a.input.val(c);this._updateAlternate(a);var h=this._get(a,"onSelect");if(h)h.apply(a.input?a.input[0]:null,[c,a]);else a.input&&a.input.trigger("change");if(a.inline)this._updateDatepicker(a);else{this._hideDatepicker();
this._lastInput=a.input[0];typeof a.input[0]!="object"&&a.input.focus();this._lastInput=null}},_updateAlternate:function(a){var c=this._get(a,"altField");if(c){var h=this._get(a,"altFormat")||this._get(a,"dateFormat"),i=this._getDate(a),j=this.formatDate(h,i,this._getFormatConfig(a));b(c).each(function(){b(this).val(j)})}},noWeekends:function(a){a=a.getDay();return[a>0&&a<6,""]},iso8601Week:function(a){a=new Date(a.getTime());a.setDate(a.getDate()+4-(a.getDay()||7));var c=a.getTime();a.setMonth(0);
a.setDate(1);return Math.floor(Math.round((c-a)/864E5)/7)+1},parseDate:function(a,c,h){if(a==null||c==null)throw"Invalid arguments";c=typeof c=="object"?c.toString():c+"";if(c=="")return null;var i=(h?h.shortYearCutoff:null)||this._defaults.shortYearCutoff;i=typeof i!="string"?i:(new Date).getFullYear()%100+parseInt(i,10);for(var j=(h?h.dayNamesShort:null)||this._defaults.dayNamesShort,n=(h?h.dayNames:null)||this._defaults.dayNames,p=(h?h.monthNamesShort:null)||this._defaults.monthNamesShort,l=(h?
h.monthNames:null)||this._defaults.monthNames,k=h=-1,m=-1,o=-1,q=false,s=function(x){(x=y+1<a.length&&a.charAt(y+1)==x)&&y++;return x},r=function(x){var C=s(x);x=new RegExp("^\\d{1,"+(x=="@"?14:x=="!"?20:x=="y"&&C?4:x=="o"?3:2)+"}");x=c.substring(w).match(x);if(!x)throw"Missing number at position "+w;w+=x[0].length;return parseInt(x[0],10)},u=function(x,C,J){x=s(x)?J:C;for(C=0;C<x.length;C++)if(c.substr(w,x[C].length).toLowerCase()==x[C].toLowerCase()){w+=x[C].length;return C+1}throw"Unknown name at position "+
w;},v=function(){if(c.charAt(w)!=a.charAt(y))throw"Unexpected literal at position "+w;w++},w=0,y=0;y<a.length;y++)if(q)if(a.charAt(y)=="'"&&!s("'"))q=false;else v();else switch(a.charAt(y)){case "d":m=r("d");break;case "D":u("D",j,n);break;case "o":o=r("o");break;case "m":k=r("m");break;case "M":k=u("M",p,l);break;case "y":h=r("y");break;case "@":var B=new Date(r("@"));h=B.getFullYear();k=B.getMonth()+1;m=B.getDate();break;case "!":B=new Date((r("!")-this._ticksTo1970)/1E4);h=B.getFullYear();k=B.getMonth()+
1;m=B.getDate();break;case "'":if(s("'"))v();else q=true;break;default:v()}if(h==-1)h=(new Date).getFullYear();else if(h<100)h+=(new Date).getFullYear()-(new Date).getFullYear()%100+(h<=i?0:-100);if(o>-1){k=1;m=o;do{i=this._getDaysInMonth(h,k-1);if(m<=i)break;k++;m-=i}while(1)}B=this._daylightSavingAdjust(new Date(h,k-1,m));if(B.getFullYear()!=h||B.getMonth()+1!=k||B.getDate()!=m)throw"Invalid date";return B},ATOM:"yy-mm-dd",COOKIE:"D, dd M yy",ISO_8601:"yy-mm-dd",RFC_822:"D, d M y",RFC_850:"DD, dd-M-y",
RFC_1036:"D, d M y",RFC_1123:"D, d M yy",RFC_2822:"D, d M yy",RSS:"D, d M y",TICKS:"!",TIMESTAMP:"@",W3C:"yy-mm-dd",_ticksTo1970:(718685+Math.floor(492.5)-Math.floor(19.7)+Math.floor(4.925))*24*60*60*1E7,formatDate:function(a,c,h){if(!c)return"";var i=(h?h.dayNamesShort:null)||this._defaults.dayNamesShort,j=(h?h.dayNames:null)||this._defaults.dayNames,n=(h?h.monthNamesShort:null)||this._defaults.monthNamesShort;h=(h?h.monthNames:null)||this._defaults.monthNames;var p=function(s){(s=q+1<a.length&&
a.charAt(q+1)==s)&&q++;return s},l=function(s,r,u){r=""+r;if(p(s))for(;r.length<u;)r="0"+r;return r},k=function(s,r,u,v){return p(s)?v[r]:u[r]},m="",o=false;if(c)for(var q=0;q<a.length;q++)if(o)if(a.charAt(q)=="'"&&!p("'"))o=false;else m+=a.charAt(q);else switch(a.charAt(q)){case "d":m+=l("d",c.getDate(),2);break;case "D":m+=k("D",c.getDay(),i,j);break;case "o":m+=l("o",(c.getTime()-(new Date(c.getFullYear(),0,0)).getTime())/864E5,3);break;case "m":m+=l("m",c.getMonth()+1,2);break;case "M":m+=k("M",
c.getMonth(),n,h);break;case "y":m+=p("y")?c.getFullYear():(c.getYear()%100<10?"0":"")+c.getYear()%100;break;case "@":m+=c.getTime();break;case "!":m+=c.getTime()*1E4+this._ticksTo1970;break;case "'":if(p("'"))m+="'";else o=true;break;default:m+=a.charAt(q)}return m},_possibleChars:function(a){for(var c="",h=false,i=function(n){(n=j+1<a.length&&a.charAt(j+1)==n)&&j++;return n},j=0;j<a.length;j++)if(h)if(a.charAt(j)=="'"&&!i("'"))h=false;else c+=a.charAt(j);else switch(a.charAt(j)){case "d":case "m":case "y":case "@":c+=
"0123456789";break;case "D":case "M":return null;case "'":if(i("'"))c+="'";else h=true;break;default:c+=a.charAt(j)}return c},_get:function(a,c){return a.settings[c]!==d?a.settings[c]:this._defaults[c]},_setDateFromField:function(a,c){if(a.input.val()!=a.lastVal){var h=this._get(a,"dateFormat"),i=a.lastVal=a.input?a.input.val():null,j,n;j=n=this._getDefaultDate(a);var p=this._getFormatConfig(a);try{j=this.parseDate(h,i,p)||n}catch(l){this.log(l);i=c?"":i}a.selectedDay=j.getDate();a.drawMonth=a.selectedMonth=
j.getMonth();a.drawYear=a.selectedYear=j.getFullYear();a.currentDay=i?j.getDate():0;a.currentMonth=i?j.getMonth():0;a.currentYear=i?j.getFullYear():0;this._adjustInstDate(a)}},_getDefaultDate:function(a){return this._restrictMinMax(a,this._determineDate(a,this._get(a,"defaultDate"),new Date))},_determineDate:function(a,c,h){var i=function(n){var p=new Date;p.setDate(p.getDate()+n);return p},j=function(n){try{return b.datepicker.parseDate(b.datepicker._get(a,"dateFormat"),n,b.datepicker._getFormatConfig(a))}catch(p){}var l=
(n.toLowerCase().match(/^c/)?b.datepicker._getDate(a):null)||new Date,k=l.getFullYear(),m=l.getMonth();l=l.getDate();for(var o=/([+-]?[0-9]+)\s*(d|D|w|W|m|M|y|Y)?/g,q=o.exec(n);q;){switch(q[2]||"d"){case "d":case "D":l+=parseInt(q[1],10);break;case "w":case "W":l+=parseInt(q[1],10)*7;break;case "m":case "M":m+=parseInt(q[1],10);l=Math.min(l,b.datepicker._getDaysInMonth(k,m));break;case "y":case "Y":k+=parseInt(q[1],10);l=Math.min(l,b.datepicker._getDaysInMonth(k,m));break}q=o.exec(n)}return new Date(k,
m,l)};if(c=(c=c==null||c===""?h:typeof c=="string"?j(c):typeof c=="number"?isNaN(c)?h:i(c):new Date(c.getTime()))&&c.toString()=="Invalid Date"?h:c){c.setHours(0);c.setMinutes(0);c.setSeconds(0);c.setMilliseconds(0)}return this._daylightSavingAdjust(c)},_daylightSavingAdjust:function(a){if(!a)return null;a.setHours(a.getHours()>12?a.getHours()+2:0);return a},_setDate:function(a,c,h){var i=!c,j=a.selectedMonth,n=a.selectedYear;c=this._restrictMinMax(a,this._determineDate(a,c,new Date));a.selectedDay=
a.currentDay=c.getDate();a.drawMonth=a.selectedMonth=a.currentMonth=c.getMonth();a.drawYear=a.selectedYear=a.currentYear=c.getFullYear();if((j!=a.selectedMonth||n!=a.selectedYear)&&!h)this._notifyChange(a);this._adjustInstDate(a);if(a.input)a.input.val(i?"":this._formatDate(a))},_getDate:function(a){return!a.currentYear||a.input&&a.input.val()==""?null:this._daylightSavingAdjust(new Date(a.currentYear,a.currentMonth,a.currentDay))},_generateHTML:function(a){var c=new Date;c=this._daylightSavingAdjust(new Date(c.getFullYear(),
c.getMonth(),c.getDate()));var h=this._get(a,"isRTL"),i=this._get(a,"showButtonPanel"),j=this._get(a,"hideIfNoPrevNext"),n=this._get(a,"navigationAsDateFormat"),p=this._getNumberOfMonths(a),l=this._get(a,"showCurrentAtPos"),k=this._get(a,"stepMonths"),m=p[0]!=1||p[1]!=1,o=this._daylightSavingAdjust(!a.currentDay?new Date(9999,9,9):new Date(a.currentYear,a.currentMonth,a.currentDay)),q=this._getMinMaxDate(a,"min"),s=this._getMinMaxDate(a,"max");l=a.drawMonth-l;var r=a.drawYear;if(l<0){l+=12;r--}if(s){var u=
this._daylightSavingAdjust(new Date(s.getFullYear(),s.getMonth()-p[0]*p[1]+1,s.getDate()));for(u=q&&u<q?q:u;this._daylightSavingAdjust(new Date(r,l,1))>u;){l--;if(l<0){l=11;r--}}}a.drawMonth=l;a.drawYear=r;u=this._get(a,"prevText");u=!n?u:this.formatDate(u,this._daylightSavingAdjust(new Date(r,l-k,1)),this._getFormatConfig(a));u=this._canAdjustMonth(a,-1,r,l)?'<a class="ui-datepicker-prev ui-corner-all" onclick="DP_jQuery_'+f+".datepicker._adjustDate('#"+a.id+"', -"+k+", 'M');\" title=\""+u+'"><span class="ui-icon ui-icon-circle-triangle-'+
(h?"e":"w")+'">'+u+"</span></a>":j?"":'<a class="ui-datepicker-prev ui-corner-all ui-state-disabled" title="'+u+'"><span class="ui-icon ui-icon-circle-triangle-'+(h?"e":"w")+'">'+u+"</span></a>";var v=this._get(a,"nextText");v=!n?v:this.formatDate(v,this._daylightSavingAdjust(new Date(r,l+k,1)),this._getFormatConfig(a));j=this._canAdjustMonth(a,+1,r,l)?'<a class="ui-datepicker-next ui-corner-all" onclick="DP_jQuery_'+f+".datepicker._adjustDate('#"+a.id+"', +"+k+", 'M');\" title=\""+v+'"><span class="ui-icon ui-icon-circle-triangle-'+
(h?"w":"e")+'">'+v+"</span></a>":j?"":'<a class="ui-datepicker-next ui-corner-all ui-state-disabled" title="'+v+'"><span class="ui-icon ui-icon-circle-triangle-'+(h?"w":"e")+'">'+v+"</span></a>";k=this._get(a,"currentText");v=this._get(a,"gotoCurrent")&&a.currentDay?o:c;k=!n?k:this.formatDate(k,v,this._getFormatConfig(a));n=!a.inline?'<button type="button" class="ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all" onclick="DP_jQuery_'+f+'.datepicker._hideDatepicker();">'+this._get(a,
"closeText")+"</button>":"";i=i?'<div class="ui-datepicker-buttonpane ui-widget-content">'+(h?n:"")+(this._isInRange(a,v)?'<button type="button" class="ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all" onclick="DP_jQuery_'+f+".datepicker._gotoToday('#"+a.id+"');\">"+k+"</button>":"")+(h?"":n)+"</div>":"";n=parseInt(this._get(a,"firstDay"),10);n=isNaN(n)?0:n;k=this._get(a,"showWeek");v=this._get(a,"dayNames");this._get(a,"dayNamesShort");var w=this._get(a,"dayNamesMin"),y=
this._get(a,"monthNames"),B=this._get(a,"monthNamesShort"),x=this._get(a,"beforeShowDay"),C=this._get(a,"showOtherMonths"),J=this._get(a,"selectOtherMonths");this._get(a,"calculateWeek");for(var M=this._getDefaultDate(a),K="",G=0;G<p[0];G++){for(var N="",H=0;H<p[1];H++){var O=this._daylightSavingAdjust(new Date(r,l,a.selectedDay)),A=" ui-corner-all",D="";if(m){D+='<div class="ui-datepicker-group';if(p[1]>1)switch(H){case 0:D+=" ui-datepicker-group-first";A=" ui-corner-"+(h?"right":"left");break;case p[1]-
1:D+=" ui-datepicker-group-last";A=" ui-corner-"+(h?"left":"right");break;default:D+=" ui-datepicker-group-middle";A="";break}D+='">'}D+='<div class="ui-datepicker-header ui-widget-header ui-helper-clearfix'+A+'">'+(/all|left/.test(A)&&G==0?h?j:u:"")+(/all|right/.test(A)&&G==0?h?u:j:"")+this._generateMonthYearHeader(a,l,r,q,s,G>0||H>0,y,B)+'</div><table class="ui-datepicker-calendar"><thead><tr>';var E=k?'<th class="ui-datepicker-week-col">'+this._get(a,"weekHeader")+"</th>":"";for(A=0;A<7;A++){var z=
(A+n)%7;E+="<th"+((A+n+6)%7>=5?' class="ui-datepicker-week-end"':"")+'><span title="'+v[z]+'">'+w[z]+"</span></th>"}D+=E+"</tr></thead><tbody>";E=this._getDaysInMonth(r,l);if(r==a.selectedYear&&l==a.selectedMonth)a.selectedDay=Math.min(a.selectedDay,E);A=(this._getFirstDayOfMonth(r,l)-n+7)%7;E=m?6:Math.ceil((A+E)/7);z=this._daylightSavingAdjust(new Date(r,l,1-A));for(var P=0;P<E;P++){D+="<tr>";var Q=!k?"":'<td class="ui-datepicker-week-col">'+this._get(a,"calculateWeek")(z)+"</td>";for(A=0;A<7;A++){var I=
x?x.apply(a.input?a.input[0]:null,[z]):[true,""],F=z.getMonth()!=l,L=F&&!J||!I[0]||q&&z<q||s&&z>s;Q+='<td class="'+((A+n+6)%7>=5?" ui-datepicker-week-end":"")+(F?" ui-datepicker-other-month":"")+(z.getTime()==O.getTime()&&l==a.selectedMonth&&a._keyEvent||M.getTime()==z.getTime()&&M.getTime()==O.getTime()?" "+this._dayOverClass:"")+(L?" "+this._unselectableClass+" ui-state-disabled":"")+(F&&!C?"":" "+I[1]+(z.getTime()==o.getTime()?" "+this._currentClass:"")+(z.getTime()==c.getTime()?" ui-datepicker-today":
""))+'"'+((!F||C)&&I[2]?' title="'+I[2]+'"':"")+(L?"":' onclick="DP_jQuery_'+f+".datepicker._selectDay('#"+a.id+"',"+z.getMonth()+","+z.getFullYear()+', this);return false;"')+">"+(F&&!C?"&#xa0;":L?'<span class="ui-state-default">'+z.getDate()+"</span>":'<a class="ui-state-default'+(z.getTime()==c.getTime()?" ui-state-highlight":"")+(z.getTime()==o.getTime()?" ui-state-active":"")+(F?" ui-priority-secondary":"")+'" href="#">'+z.getDate()+"</a>")+"</td>";z.setDate(z.getDate()+1);z=this._daylightSavingAdjust(z)}D+=
Q+"</tr>"}l++;if(l>11){l=0;r++}D+="</tbody></table>"+(m?"</div>"+(p[0]>0&&H==p[1]-1?'<div class="ui-datepicker-row-break"></div>':""):"");N+=D}K+=N}K+=i+(b.browser.msie&&parseInt(b.browser.version,10)<7&&!a.inline?'<iframe src="javascript:false;" class="ui-datepicker-cover" frameborder="0"></iframe>':"");a._keyEvent=false;return K},_generateMonthYearHeader:function(a,c,h,i,j,n,p,l){var k=this._get(a,"changeMonth"),m=this._get(a,"changeYear"),o=this._get(a,"showMonthAfterYear"),q='<div class="ui-datepicker-title">',
s="";if(n||!k)s+='<span class="ui-datepicker-month">'+p[c]+"</span>";else{p=i&&i.getFullYear()==h;var r=j&&j.getFullYear()==h;s+='<select class="ui-datepicker-month" onchange="DP_jQuery_'+f+".datepicker._selectMonthYear('#"+a.id+"', this, 'M');\" onclick=\"DP_jQuery_"+f+".datepicker._clickMonthYear('#"+a.id+"');\">";for(var u=0;u<12;u++)if((!p||u>=i.getMonth())&&(!r||u<=j.getMonth()))s+='<option value="'+u+'"'+(u==c?' selected="selected"':"")+">"+l[u]+"</option>";s+="</select>"}o||(q+=s+(n||!(k&&
m)?"&#xa0;":""));a.yearshtml="";if(n||!m)q+='<span class="ui-datepicker-year">'+h+"</span>";else{l=this._get(a,"yearRange").split(":");var v=(new Date).getFullYear();p=function(w){w=w.match(/c[+-].*/)?h+parseInt(w.substring(1),10):w.match(/[+-].*/)?v+parseInt(w,10):parseInt(w,10);return isNaN(w)?v:w};c=p(l[0]);l=Math.max(c,p(l[1]||""));c=i?Math.max(c,i.getFullYear()):c;l=j?Math.min(l,j.getFullYear()):l;for(a.yearshtml+='<select class="ui-datepicker-year" onchange="DP_jQuery_'+f+".datepicker._selectMonthYear('#"+
a.id+"', this, 'Y');\" onclick=\"DP_jQuery_"+f+".datepicker._clickMonthYear('#"+a.id+"');\">";c<=l;c++)a.yearshtml+='<option value="'+c+'"'+(c==h?' selected="selected"':"")+">"+c+"</option>";a.yearshtml+="</select>";if(b.browser.mozilla)q+='<select class="ui-datepicker-year"><option value="'+h+'" selected="selected">'+h+"</option></select>";else{q+=a.yearshtml;a.yearshtml=null}}q+=this._get(a,"yearSuffix");if(o)q+=(n||!(k&&m)?"&#xa0;":"")+s;q+="</div>";return q},_adjustInstDate:function(a,c,h){var i=
a.drawYear+(h=="Y"?c:0),j=a.drawMonth+(h=="M"?c:0);c=Math.min(a.selectedDay,this._getDaysInMonth(i,j))+(h=="D"?c:0);i=this._restrictMinMax(a,this._daylightSavingAdjust(new Date(i,j,c)));a.selectedDay=i.getDate();a.drawMonth=a.selectedMonth=i.getMonth();a.drawYear=a.selectedYear=i.getFullYear();if(h=="M"||h=="Y")this._notifyChange(a)},_restrictMinMax:function(a,c){var h=this._getMinMaxDate(a,"min");a=this._getMinMaxDate(a,"max");c=h&&c<h?h:c;return c=a&&c>a?a:c},_notifyChange:function(a){var c=this._get(a,
"onChangeMonthYear");if(c)c.apply(a.input?a.input[0]:null,[a.selectedYear,a.selectedMonth+1,a])},_getNumberOfMonths:function(a){a=this._get(a,"numberOfMonths");return a==null?[1,1]:typeof a=="number"?[1,a]:a},_getMinMaxDate:function(a,c){return this._determineDate(a,this._get(a,c+"Date"),null)},_getDaysInMonth:function(a,c){return 32-this._daylightSavingAdjust(new Date(a,c,32)).getDate()},_getFirstDayOfMonth:function(a,c){return(new Date(a,c,1)).getDay()},_canAdjustMonth:function(a,c,h,i){var j=this._getNumberOfMonths(a);
h=this._daylightSavingAdjust(new Date(h,i+(c<0?c:j[0]*j[1]),1));c<0&&h.setDate(this._getDaysInMonth(h.getFullYear(),h.getMonth()));return this._isInRange(a,h)},_isInRange:function(a,c){var h=this._getMinMaxDate(a,"min");a=this._getMinMaxDate(a,"max");return(!h||c.getTime()>=h.getTime())&&(!a||c.getTime()<=a.getTime())},_getFormatConfig:function(a){var c=this._get(a,"shortYearCutoff");c=typeof c!="string"?c:(new Date).getFullYear()%100+parseInt(c,10);return{shortYearCutoff:c,dayNamesShort:this._get(a,
"dayNamesShort"),dayNames:this._get(a,"dayNames"),monthNamesShort:this._get(a,"monthNamesShort"),monthNames:this._get(a,"monthNames")}},_formatDate:function(a,c,h,i){if(!c){a.currentDay=a.selectedDay;a.currentMonth=a.selectedMonth;a.currentYear=a.selectedYear}c=c?typeof c=="object"?c:this._daylightSavingAdjust(new Date(i,h,c)):this._daylightSavingAdjust(new Date(a.currentYear,a.currentMonth,a.currentDay));return this.formatDate(this._get(a,"dateFormat"),c,this._getFormatConfig(a))}});b.fn.datepicker=
function(a){if(!this.length)return this;if(!b.datepicker.initialized){b(document).mousedown(b.datepicker._checkExternalClick).find("body").append(b.datepicker.dpDiv);b.datepicker.initialized=true}var c=Array.prototype.slice.call(arguments,1);if(typeof a=="string"&&(a=="isDisabled"||a=="getDate"||a=="widget"))return b.datepicker["_"+a+"Datepicker"].apply(b.datepicker,[this[0]].concat(c));if(a=="option"&&arguments.length==2&&typeof arguments[1]=="string")return b.datepicker["_"+a+"Datepicker"].apply(b.datepicker,
[this[0]].concat(c));return this.each(function(){typeof a=="string"?b.datepicker["_"+a+"Datepicker"].apply(b.datepicker,[this].concat(c)):b.datepicker._attachDatepicker(this,a)})};b.datepicker=new e;b.datepicker.initialized=false;b.datepicker.uuid=(new Date).getTime();b.datepicker.version="1.8.11";window["DP_jQuery_"+f]=b})(jQuery);
(function(b,d){var e={buttons:true,height:true,maxHeight:true,maxWidth:true,minHeight:true,minWidth:true,width:true},g={maxHeight:true,maxWidth:true,minHeight:true,minWidth:true};b.widget("ui.dialog",{options:{autoOpen:true,buttons:{},closeOnEscape:true,closeText:"close",dialogClass:"",draggable:true,hide:null,height:"auto",maxHeight:false,maxWidth:false,minHeight:150,minWidth:150,modal:false,position:{my:"center",at:"center",collision:"fit",using:function(f){var a=b(this).css(f).offset().top;a<0&&
b(this).css("top",f.top-a)}},resizable:true,show:null,stack:true,title:"",width:300,zIndex:1E3},_create:function(){this.originalTitle=this.element.attr("title");if(typeof this.originalTitle!=="string")this.originalTitle="";this.options.title=this.options.title||this.originalTitle;var f=this,a=f.options,c=a.title||"&#160;",h=b.ui.dialog.getTitleId(f.element),i=(f.uiDialog=b("<div></div>")).appendTo(document.body).hide().addClass("ui-dialog ui-widget ui-widget-content ui-corner-all "+a.dialogClass).css({zIndex:a.zIndex}).attr("tabIndex",
-1).css("outline",0).keydown(function(p){if(a.closeOnEscape&&p.keyCode&&p.keyCode===b.ui.keyCode.ESCAPE){f.close(p);p.preventDefault()}}).attr({role:"dialog","aria-labelledby":h}).mousedown(function(p){f.moveToTop(false,p)});f.element.show().removeAttr("title").addClass("ui-dialog-content ui-widget-content").appendTo(i);var j=(f.uiDialogTitlebar=b("<div></div>")).addClass("ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix").prependTo(i),n=b('<a href="#"></a>').addClass("ui-dialog-titlebar-close ui-corner-all").attr("role",
"button").hover(function(){n.addClass("ui-state-hover")},function(){n.removeClass("ui-state-hover")}).focus(function(){n.addClass("ui-state-focus")}).blur(function(){n.removeClass("ui-state-focus")}).click(function(p){f.close(p);return false}).appendTo(j);(f.uiDialogTitlebarCloseText=b("<span></span>")).addClass("ui-icon ui-icon-closethick").text(a.closeText).appendTo(n);b("<span></span>").addClass("ui-dialog-title").attr("id",h).html(c).prependTo(j);if(b.isFunction(a.beforeclose)&&!b.isFunction(a.beforeClose))a.beforeClose=
a.beforeclose;j.find("*").add(j).disableSelection();a.draggable&&b.fn.draggable&&f._makeDraggable();a.resizable&&b.fn.resizable&&f._makeResizable();f._createButtons(a.buttons);f._isOpen=false;b.fn.bgiframe&&i.bgiframe()},_init:function(){this.options.autoOpen&&this.open()},destroy:function(){var f=this;f.overlay&&f.overlay.destroy();f.uiDialog.hide();f.element.unbind(".dialog").removeData("dialog").removeClass("ui-dialog-content ui-widget-content").hide().appendTo("body");f.uiDialog.remove();f.originalTitle&&
f.element.attr("title",f.originalTitle);return f},widget:function(){return this.uiDialog},close:function(f){var a=this,c,h;if(false!==a._trigger("beforeClose",f)){a.overlay&&a.overlay.destroy();a.uiDialog.unbind("keypress.ui-dialog");a._isOpen=false;if(a.options.hide)a.uiDialog.hide(a.options.hide,function(){a._trigger("close",f)});else{a.uiDialog.hide();a._trigger("close",f)}b.ui.dialog.overlay.resize();if(a.options.modal){c=0;b(".ui-dialog").each(function(){if(this!==a.uiDialog[0]){h=b(this).css("z-index");
isNaN(h)||(c=Math.max(c,h))}});b.ui.dialog.maxZ=c}return a}},isOpen:function(){return this._isOpen},moveToTop:function(f,a){var c=this,h=c.options;if(h.modal&&!f||!h.stack&&!h.modal)return c._trigger("focus",a);if(h.zIndex>b.ui.dialog.maxZ)b.ui.dialog.maxZ=h.zIndex;if(c.overlay){b.ui.dialog.maxZ+=1;c.overlay.$el.css("z-index",b.ui.dialog.overlay.maxZ=b.ui.dialog.maxZ)}f={scrollTop:c.element.attr("scrollTop"),scrollLeft:c.element.attr("scrollLeft")};b.ui.dialog.maxZ+=1;c.uiDialog.css("z-index",b.ui.dialog.maxZ);
c.element.attr(f);c._trigger("focus",a);return c},open:function(){if(!this._isOpen){var f=this,a=f.options,c=f.uiDialog;f.overlay=a.modal?new b.ui.dialog.overlay(f):null;f._size();f._position(a.position);c.show(a.show);f.moveToTop(true);a.modal&&c.bind("keypress.ui-dialog",function(h){if(h.keyCode===b.ui.keyCode.TAB){var i=b(":tabbable",this),j=i.filter(":first");i=i.filter(":last");if(h.target===i[0]&&!h.shiftKey){j.focus(1);return false}else if(h.target===j[0]&&h.shiftKey){i.focus(1);return false}}});
b(f.element.find(":tabbable").get().concat(c.find(".ui-dialog-buttonpane :tabbable").get().concat(c.get()))).eq(0).focus();f._isOpen=true;f._trigger("open");return f}},_createButtons:function(f){var a=this,c=false,h=b("<div></div>").addClass("ui-dialog-buttonpane ui-widget-content ui-helper-clearfix"),i=b("<div></div>").addClass("ui-dialog-buttonset").appendTo(h);a.uiDialog.find(".ui-dialog-buttonpane").remove();typeof f==="object"&&f!==null&&b.each(f,function(){return!(c=true)});if(c){b.each(f,function(j,
n){n=b.isFunction(n)?{click:n,text:j}:n;j=b('<button type="button"></button>').attr(n,true).unbind("click").click(function(){n.click.apply(a.element[0],arguments)}).appendTo(i);b.fn.button&&j.button()});h.appendTo(a.uiDialog)}},_makeDraggable:function(){function f(j){return{position:j.position,offset:j.offset}}var a=this,c=a.options,h=b(document),i;a.uiDialog.draggable({cancel:".ui-dialog-content, .ui-dialog-titlebar-close",handle:".ui-dialog-titlebar",containment:"document",start:function(j,n){i=
c.height==="auto"?"auto":b(this).height();b(this).height(b(this).height()).addClass("ui-dialog-dragging");a._trigger("dragStart",j,f(n))},drag:function(j,n){a._trigger("drag",j,f(n))},stop:function(j,n){c.position=[n.position.left-h.scrollLeft(),n.position.top-h.scrollTop()];b(this).removeClass("ui-dialog-dragging").height(i);a._trigger("dragStop",j,f(n));b.ui.dialog.overlay.resize()}})},_makeResizable:function(f){function a(j){return{originalPosition:j.originalPosition,originalSize:j.originalSize,
position:j.position,size:j.size}}f=f===d?this.options.resizable:f;var c=this,h=c.options,i=c.uiDialog.css("position");f=typeof f==="string"?f:"n,e,s,w,se,sw,ne,nw";c.uiDialog.resizable({cancel:".ui-dialog-content",containment:"document",alsoResize:c.element,maxWidth:h.maxWidth,maxHeight:h.maxHeight,minWidth:h.minWidth,minHeight:c._minHeight(),handles:f,start:function(j,n){b(this).addClass("ui-dialog-resizing");c._trigger("resizeStart",j,a(n))},resize:function(j,n){c._trigger("resize",j,a(n))},stop:function(j,
n){b(this).removeClass("ui-dialog-resizing");h.height=b(this).height();h.width=b(this).width();c._trigger("resizeStop",j,a(n));b.ui.dialog.overlay.resize()}}).css("position",i).find(".ui-resizable-se").addClass("ui-icon ui-icon-grip-diagonal-se")},_minHeight:function(){var f=this.options;return f.height==="auto"?f.minHeight:Math.min(f.minHeight,f.height)},_position:function(f){var a=[],c=[0,0],h;if(f){if(typeof f==="string"||typeof f==="object"&&"0"in f){a=f.split?f.split(" "):[f[0],f[1]];if(a.length===
1)a[1]=a[0];b.each(["left","top"],function(i,j){if(+a[i]===a[i]){c[i]=a[i];a[i]=j}});f={my:a.join(" "),at:a.join(" "),offset:c.join(" ")}}f=b.extend({},b.ui.dialog.prototype.options.position,f)}else f=b.ui.dialog.prototype.options.position;(h=this.uiDialog.is(":visible"))||this.uiDialog.show();this.uiDialog.css({top:0,left:0}).position(b.extend({of:window},f));h||this.uiDialog.hide()},_setOptions:function(f){var a=this,c={},h=false;b.each(f,function(i,j){a._setOption(i,j);if(i in e)h=true;if(i in
g)c[i]=j});h&&this._size();this.uiDialog.is(":data(resizable)")&&this.uiDialog.resizable("option",c)},_setOption:function(f,a){var c=this,h=c.uiDialog;switch(f){case "beforeclose":f="beforeClose";break;case "buttons":c._createButtons(a);break;case "closeText":c.uiDialogTitlebarCloseText.text(""+a);break;case "dialogClass":h.removeClass(c.options.dialogClass).addClass("ui-dialog ui-widget ui-widget-content ui-corner-all "+a);break;case "disabled":a?h.addClass("ui-dialog-disabled"):h.removeClass("ui-dialog-disabled");
break;case "draggable":var i=h.is(":data(draggable)");i&&!a&&h.draggable("destroy");!i&&a&&c._makeDraggable();break;case "position":c._position(a);break;case "resizable":(i=h.is(":data(resizable)"))&&!a&&h.resizable("destroy");i&&typeof a==="string"&&h.resizable("option","handles",a);!i&&a!==false&&c._makeResizable(a);break;case "title":b(".ui-dialog-title",c.uiDialogTitlebar).html(""+(a||"&#160;"));break}b.Widget.prototype._setOption.apply(c,arguments)},_size:function(){var f=this.options,a,c,h=
this.uiDialog.is(":visible");this.element.show().css({width:"auto",minHeight:0,height:0});if(f.minWidth>f.width)f.width=f.minWidth;a=this.uiDialog.css({height:"auto",width:f.width}).height();c=Math.max(0,f.minHeight-a);if(f.height==="auto")if(b.support.minHeight)this.element.css({minHeight:c,height:"auto"});else{this.uiDialog.show();f=this.element.css("height","auto").height();h||this.uiDialog.hide();this.element.height(Math.max(f,c))}else this.element.height(Math.max(f.height-a,0));this.uiDialog.is(":data(resizable)")&&
this.uiDialog.resizable("option","minHeight",this._minHeight())}});b.extend(b.ui.dialog,{version:"1.8.11",uuid:0,maxZ:0,getTitleId:function(f){f=f.attr("id");if(!f){this.uuid+=1;f=this.uuid}return"ui-dialog-title-"+f},overlay:function(f){this.$el=b.ui.dialog.overlay.create(f)}});b.extend(b.ui.dialog.overlay,{instances:[],oldInstances:[],maxZ:0,events:b.map("focus,mousedown,mouseup,keydown,keypress,click".split(","),function(f){return f+".dialog-overlay"}).join(" "),create:function(f){if(this.instances.length===
0){setTimeout(function(){b.ui.dialog.overlay.instances.length&&b(document).bind(b.ui.dialog.overlay.events,function(c){if(b(c.target).zIndex()<b.ui.dialog.overlay.maxZ)return false})},1);b(document).bind("keydown.dialog-overlay",function(c){if(f.options.closeOnEscape&&c.keyCode&&c.keyCode===b.ui.keyCode.ESCAPE){f.close(c);c.preventDefault()}});b(window).bind("resize.dialog-overlay",b.ui.dialog.overlay.resize)}var a=(this.oldInstances.pop()||b("<div></div>").addClass("ui-widget-overlay")).appendTo(document.body).css({width:this.width(),
height:this.height()});b.fn.bgiframe&&a.bgiframe();this.instances.push(a);return a},destroy:function(f){var a=b.inArray(f,this.instances);a!=-1&&this.oldInstances.push(this.instances.splice(a,1)[0]);this.instances.length===0&&b([document,window]).unbind(".dialog-overlay");f.remove();var c=0;b.each(this.instances,function(){c=Math.max(c,this.css("z-index"))});this.maxZ=c},height:function(){var f,a;if(b.browser.msie&&b.browser.version<7){f=Math.max(document.documentElement.scrollHeight,document.body.scrollHeight);
a=Math.max(document.documentElement.offsetHeight,document.body.offsetHeight);return f<a?b(window).height()+"px":f+"px"}else return b(document).height()+"px"},width:function(){var f,a;if(b.browser.msie&&b.browser.version<7){f=Math.max(document.documentElement.scrollWidth,document.body.scrollWidth);a=Math.max(document.documentElement.offsetWidth,document.body.offsetWidth);return f<a?b(window).width()+"px":f+"px"}else return b(document).width()+"px"},resize:function(){var f=b([]);b.each(b.ui.dialog.overlay.instances,
function(){f=f.add(this)});f.css({width:0,height:0}).css({width:b.ui.dialog.overlay.width(),height:b.ui.dialog.overlay.height()})}});b.extend(b.ui.dialog.overlay.prototype,{destroy:function(){b.ui.dialog.overlay.destroy(this.$el)}})})(jQuery);
(function(b){b.ui=b.ui||{};var d=/left|center|right/,e=/top|center|bottom/,g=b.fn.position,f=b.fn.offset;b.fn.position=function(a){if(!a||!a.of)return g.apply(this,arguments);a=b.extend({},a);var c=b(a.of),h=c[0],i=(a.collision||"flip").split(" "),j=a.offset?a.offset.split(" "):[0,0],n,p,l;if(h.nodeType===9){n=c.width();p=c.height();l={top:0,left:0}}else if(h.setTimeout){n=c.width();p=c.height();l={top:c.scrollTop(),left:c.scrollLeft()}}else if(h.preventDefault){a.at="left top";n=p=0;l={top:a.of.pageY,
left:a.of.pageX}}else{n=c.outerWidth();p=c.outerHeight();l=c.offset()}b.each(["my","at"],function(){var k=(a[this]||"").split(" ");if(k.length===1)k=d.test(k[0])?k.concat(["center"]):e.test(k[0])?["center"].concat(k):["center","center"];k[0]=d.test(k[0])?k[0]:"center";k[1]=e.test(k[1])?k[1]:"center";a[this]=k});if(i.length===1)i[1]=i[0];j[0]=parseInt(j[0],10)||0;if(j.length===1)j[1]=j[0];j[1]=parseInt(j[1],10)||0;if(a.at[0]==="right")l.left+=n;else if(a.at[0]==="center")l.left+=n/2;if(a.at[1]==="bottom")l.top+=
p;else if(a.at[1]==="center")l.top+=p/2;l.left+=j[0];l.top+=j[1];return this.each(function(){var k=b(this),m=k.outerWidth(),o=k.outerHeight(),q=parseInt(b.curCSS(this,"marginLeft",true))||0,s=parseInt(b.curCSS(this,"marginTop",true))||0,r=m+q+(parseInt(b.curCSS(this,"marginRight",true))||0),u=o+s+(parseInt(b.curCSS(this,"marginBottom",true))||0),v=b.extend({},l),w;if(a.my[0]==="right")v.left-=m;else if(a.my[0]==="center")v.left-=m/2;if(a.my[1]==="bottom")v.top-=o;else if(a.my[1]==="center")v.top-=
o/2;v.left=Math.round(v.left);v.top=Math.round(v.top);w={left:v.left-q,top:v.top-s};b.each(["left","top"],function(y,B){b.ui.position[i[y]]&&b.ui.position[i[y]][B](v,{targetWidth:n,targetHeight:p,elemWidth:m,elemHeight:o,collisionPosition:w,collisionWidth:r,collisionHeight:u,offset:j,my:a.my,at:a.at})});b.fn.bgiframe&&k.bgiframe();k.offset(b.extend(v,{using:a.using}))})};b.ui.position={fit:{left:function(a,c){var h=b(window);h=c.collisionPosition.left+c.collisionWidth-h.width()-h.scrollLeft();a.left=
h>0?a.left-h:Math.max(a.left-c.collisionPosition.left,a.left)},top:function(a,c){var h=b(window);h=c.collisionPosition.top+c.collisionHeight-h.height()-h.scrollTop();a.top=h>0?a.top-h:Math.max(a.top-c.collisionPosition.top,a.top)}},flip:{left:function(a,c){if(c.at[0]!=="center"){var h=b(window);h=c.collisionPosition.left+c.collisionWidth-h.width()-h.scrollLeft();var i=c.my[0]==="left"?-c.elemWidth:c.my[0]==="right"?c.elemWidth:0,j=c.at[0]==="left"?c.targetWidth:-c.targetWidth,n=-2*c.offset[0];a.left+=
c.collisionPosition.left<0?i+j+n:h>0?i+j+n:0}},top:function(a,c){if(c.at[1]!=="center"){var h=b(window);h=c.collisionPosition.top+c.collisionHeight-h.height()-h.scrollTop();var i=c.my[1]==="top"?-c.elemHeight:c.my[1]==="bottom"?c.elemHeight:0,j=c.at[1]==="top"?c.targetHeight:-c.targetHeight,n=-2*c.offset[1];a.top+=c.collisionPosition.top<0?i+j+n:h>0?i+j+n:0}}}};if(!b.offset.setOffset){b.offset.setOffset=function(a,c){if(/static/.test(b.curCSS(a,"position")))a.style.position="relative";var h=b(a),
i=h.offset(),j=parseInt(b.curCSS(a,"top",true),10)||0,n=parseInt(b.curCSS(a,"left",true),10)||0;i={top:c.top-i.top+j,left:c.left-i.left+n};"using"in c?c.using.call(a,i):h.css(i)};b.fn.offset=function(a){var c=this[0];if(!c||!c.ownerDocument)return null;if(a)return this.each(function(){b.offset.setOffset(this,a)});return f.call(this)}}})(jQuery);
(function(b,d){b.widget("ui.progressbar",{options:{value:0,max:100},min:0,_create:function(){this.element.addClass("ui-progressbar ui-widget ui-widget-content ui-corner-all").attr({role:"progressbar","aria-valuemin":this.min,"aria-valuemax":this.options.max,"aria-valuenow":this._value()});this.valueDiv=b("<div class='ui-progressbar-value ui-widget-header ui-corner-left'></div>").appendTo(this.element);this.oldValue=this._value();this._refreshValue()},destroy:function(){this.element.removeClass("ui-progressbar ui-widget ui-widget-content ui-corner-all").removeAttr("role").removeAttr("aria-valuemin").removeAttr("aria-valuemax").removeAttr("aria-valuenow");
this.valueDiv.remove();b.Widget.prototype.destroy.apply(this,arguments)},value:function(e){if(e===d)return this._value();this._setOption("value",e);return this},_setOption:function(e,g){if(e==="value"){this.options.value=g;this._refreshValue();this._value()===this.options.max&&this._trigger("complete")}b.Widget.prototype._setOption.apply(this,arguments)},_value:function(){var e=this.options.value;if(typeof e!=="number")e=0;return Math.min(this.options.max,Math.max(this.min,e))},_percentage:function(){return 100*
this._value()/this.options.max},_refreshValue:function(){var e=this.value(),g=this._percentage();if(this.oldValue!==e){this.oldValue=e;this._trigger("change")}this.valueDiv.toggleClass("ui-corner-right",e===this.options.max).width(g.toFixed(0)+"%");this.element.attr("aria-valuenow",e)}});b.extend(b.ui.progressbar,{version:"1.8.11"})})(jQuery);
(function(b){b.widget("ui.slider",b.ui.mouse,{widgetEventPrefix:"slide",options:{animate:false,distance:0,max:100,min:0,orientation:"horizontal",range:false,step:1,value:0,values:null},_create:function(){var d=this,e=this.options;this._mouseSliding=this._keySliding=false;this._animateOff=true;this._handleIndex=null;this._detectOrientation();this._mouseInit();this.element.addClass("ui-slider ui-slider-"+this.orientation+" ui-widget ui-widget-content ui-corner-all");e.disabled&&this.element.addClass("ui-slider-disabled ui-disabled");
this.range=b([]);if(e.range){if(e.range===true){this.range=b("<div></div>");if(!e.values)e.values=[this._valueMin(),this._valueMin()];if(e.values.length&&e.values.length!==2)e.values=[e.values[0],e.values[0]]}else this.range=b("<div></div>");this.range.appendTo(this.element).addClass("ui-slider-range");if(e.range==="min"||e.range==="max")this.range.addClass("ui-slider-range-"+e.range);this.range.addClass("ui-widget-header")}b(".ui-slider-handle",this.element).length===0&&b("<a href='#'></a>").appendTo(this.element).addClass("ui-slider-handle");
if(e.values&&e.values.length)for(;b(".ui-slider-handle",this.element).length<e.values.length;)b("<a href='#'></a>").appendTo(this.element).addClass("ui-slider-handle");this.handles=b(".ui-slider-handle",this.element).addClass("ui-state-default ui-corner-all");this.handle=this.handles.eq(0);this.handles.add(this.range).filter("a").click(function(g){g.preventDefault()}).hover(function(){e.disabled||b(this).addClass("ui-state-hover")},function(){b(this).removeClass("ui-state-hover")}).focus(function(){if(e.disabled)b(this).blur();
else{b(".ui-slider .ui-state-focus").removeClass("ui-state-focus");b(this).addClass("ui-state-focus")}}).blur(function(){b(this).removeClass("ui-state-focus")});this.handles.each(function(g){b(this).data("index.ui-slider-handle",g)});this.handles.keydown(function(g){var f=true,a=b(this).data("index.ui-slider-handle"),c,h,i;if(!d.options.disabled){switch(g.keyCode){case b.ui.keyCode.HOME:case b.ui.keyCode.END:case b.ui.keyCode.PAGE_UP:case b.ui.keyCode.PAGE_DOWN:case b.ui.keyCode.UP:case b.ui.keyCode.RIGHT:case b.ui.keyCode.DOWN:case b.ui.keyCode.LEFT:f=
false;if(!d._keySliding){d._keySliding=true;b(this).addClass("ui-state-active");c=d._start(g,a);if(c===false)return}break}i=d.options.step;c=d.options.values&&d.options.values.length?(h=d.values(a)):(h=d.value());switch(g.keyCode){case b.ui.keyCode.HOME:h=d._valueMin();break;case b.ui.keyCode.END:h=d._valueMax();break;case b.ui.keyCode.PAGE_UP:h=d._trimAlignValue(c+(d._valueMax()-d._valueMin())/5);break;case b.ui.keyCode.PAGE_DOWN:h=d._trimAlignValue(c-(d._valueMax()-d._valueMin())/5);break;case b.ui.keyCode.UP:case b.ui.keyCode.RIGHT:if(c===
d._valueMax())return;h=d._trimAlignValue(c+i);break;case b.ui.keyCode.DOWN:case b.ui.keyCode.LEFT:if(c===d._valueMin())return;h=d._trimAlignValue(c-i);break}d._slide(g,a,h);return f}}).keyup(function(g){var f=b(this).data("index.ui-slider-handle");if(d._keySliding){d._keySliding=false;d._stop(g,f);d._change(g,f);b(this).removeClass("ui-state-active")}});this._refreshValue();this._animateOff=false},destroy:function(){this.handles.remove();this.range.remove();this.element.removeClass("ui-slider ui-slider-horizontal ui-slider-vertical ui-slider-disabled ui-widget ui-widget-content ui-corner-all").removeData("slider").unbind(".slider");
this._mouseDestroy();return this},_mouseCapture:function(d){var e=this.options,g,f,a,c,h;if(e.disabled)return false;this.elementSize={width:this.element.outerWidth(),height:this.element.outerHeight()};this.elementOffset=this.element.offset();g=this._normValueFromMouse({x:d.pageX,y:d.pageY});f=this._valueMax()-this._valueMin()+1;c=this;this.handles.each(function(i){var j=Math.abs(g-c.values(i));if(f>j){f=j;a=b(this);h=i}});if(e.range===true&&this.values(1)===e.min){h+=1;a=b(this.handles[h])}if(this._start(d,
h)===false)return false;this._mouseSliding=true;c._handleIndex=h;a.addClass("ui-state-active").focus();e=a.offset();this._clickOffset=!b(d.target).parents().andSelf().is(".ui-slider-handle")?{left:0,top:0}:{left:d.pageX-e.left-a.width()/2,top:d.pageY-e.top-a.height()/2-(parseInt(a.css("borderTopWidth"),10)||0)-(parseInt(a.css("borderBottomWidth"),10)||0)+(parseInt(a.css("marginTop"),10)||0)};this.handles.hasClass("ui-state-hover")||this._slide(d,h,g);return this._animateOff=true},_mouseStart:function(){return true},
_mouseDrag:function(d){var e=this._normValueFromMouse({x:d.pageX,y:d.pageY});this._slide(d,this._handleIndex,e);return false},_mouseStop:function(d){this.handles.removeClass("ui-state-active");this._mouseSliding=false;this._stop(d,this._handleIndex);this._change(d,this._handleIndex);this._clickOffset=this._handleIndex=null;return this._animateOff=false},_detectOrientation:function(){this.orientation=this.options.orientation==="vertical"?"vertical":"horizontal"},_normValueFromMouse:function(d){var e;
if(this.orientation==="horizontal"){e=this.elementSize.width;d=d.x-this.elementOffset.left-(this._clickOffset?this._clickOffset.left:0)}else{e=this.elementSize.height;d=d.y-this.elementOffset.top-(this._clickOffset?this._clickOffset.top:0)}e=d/e;if(e>1)e=1;if(e<0)e=0;if(this.orientation==="vertical")e=1-e;d=this._valueMax()-this._valueMin();return this._trimAlignValue(this._valueMin()+e*d)},_start:function(d,e){var g={handle:this.handles[e],value:this.value()};if(this.options.values&&this.options.values.length){g.value=
this.values(e);g.values=this.values()}return this._trigger("start",d,g)},_slide:function(d,e,g){var f;if(this.options.values&&this.options.values.length){f=this.values(e?0:1);if(this.options.values.length===2&&this.options.range===true&&(e===0&&g>f||e===1&&g<f))g=f;if(g!==this.values(e)){f=this.values();f[e]=g;d=this._trigger("slide",d,{handle:this.handles[e],value:g,values:f});this.values(e?0:1);d!==false&&this.values(e,g,true)}}else if(g!==this.value()){d=this._trigger("slide",d,{handle:this.handles[e],
value:g});d!==false&&this.value(g)}},_stop:function(d,e){var g={handle:this.handles[e],value:this.value()};if(this.options.values&&this.options.values.length){g.value=this.values(e);g.values=this.values()}this._trigger("stop",d,g)},_change:function(d,e){if(!this._keySliding&&!this._mouseSliding){var g={handle:this.handles[e],value:this.value()};if(this.options.values&&this.options.values.length){g.value=this.values(e);g.values=this.values()}this._trigger("change",d,g)}},value:function(d){if(arguments.length){this.options.value=
this._trimAlignValue(d);this._refreshValue();this._change(null,0)}return this._value()},values:function(d,e){var g,f,a;if(arguments.length>1){this.options.values[d]=this._trimAlignValue(e);this._refreshValue();this._change(null,d)}if(arguments.length)if(b.isArray(arguments[0])){g=this.options.values;f=arguments[0];for(a=0;a<g.length;a+=1){g[a]=this._trimAlignValue(f[a]);this._change(null,a)}this._refreshValue()}else return this.options.values&&this.options.values.length?this._values(d):this.value();
else return this._values()},_setOption:function(d,e){var g,f=0;if(b.isArray(this.options.values))f=this.options.values.length;b.Widget.prototype._setOption.apply(this,arguments);switch(d){case "disabled":if(e){this.handles.filter(".ui-state-focus").blur();this.handles.removeClass("ui-state-hover");this.handles.attr("disabled","disabled");this.element.addClass("ui-disabled")}else{this.handles.removeAttr("disabled");this.element.removeClass("ui-disabled")}break;case "orientation":this._detectOrientation();
this.element.removeClass("ui-slider-horizontal ui-slider-vertical").addClass("ui-slider-"+this.orientation);this._refreshValue();break;case "value":this._animateOff=true;this._refreshValue();this._change(null,0);this._animateOff=false;break;case "values":this._animateOff=true;this._refreshValue();for(g=0;g<f;g+=1)this._change(null,g);this._animateOff=false;break}},_value:function(){var d=this.options.value;return d=this._trimAlignValue(d)},_values:function(d){var e,g;if(arguments.length){e=this.options.values[d];
return e=this._trimAlignValue(e)}else{e=this.options.values.slice();for(g=0;g<e.length;g+=1)e[g]=this._trimAlignValue(e[g]);return e}},_trimAlignValue:function(d){if(d<=this._valueMin())return this._valueMin();if(d>=this._valueMax())return this._valueMax();var e=this.options.step>0?this.options.step:1,g=(d-this._valueMin())%e;alignValue=d-g;if(Math.abs(g)*2>=e)alignValue+=g>0?e:-e;return parseFloat(alignValue.toFixed(5))},_valueMin:function(){return this.options.min},_valueMax:function(){return this.options.max},
_refreshValue:function(){var d=this.options.range,e=this.options,g=this,f=!this._animateOff?e.animate:false,a,c={},h,i,j,n;if(this.options.values&&this.options.values.length)this.handles.each(function(p){a=(g.values(p)-g._valueMin())/(g._valueMax()-g._valueMin())*100;c[g.orientation==="horizontal"?"left":"bottom"]=a+"%";b(this).stop(1,1)[f?"animate":"css"](c,e.animate);if(g.options.range===true)if(g.orientation==="horizontal"){if(p===0)g.range.stop(1,1)[f?"animate":"css"]({left:a+"%"},e.animate);
if(p===1)g.range[f?"animate":"css"]({width:a-h+"%"},{queue:false,duration:e.animate})}else{if(p===0)g.range.stop(1,1)[f?"animate":"css"]({bottom:a+"%"},e.animate);if(p===1)g.range[f?"animate":"css"]({height:a-h+"%"},{queue:false,duration:e.animate})}h=a});else{i=this.value();j=this._valueMin();n=this._valueMax();a=n!==j?(i-j)/(n-j)*100:0;c[g.orientation==="horizontal"?"left":"bottom"]=a+"%";this.handle.stop(1,1)[f?"animate":"css"](c,e.animate);if(d==="min"&&this.orientation==="horizontal")this.range.stop(1,
1)[f?"animate":"css"]({width:a+"%"},e.animate);if(d==="max"&&this.orientation==="horizontal")this.range[f?"animate":"css"]({width:100-a+"%"},{queue:false,duration:e.animate});if(d==="min"&&this.orientation==="vertical")this.range.stop(1,1)[f?"animate":"css"]({height:a+"%"},e.animate);if(d==="max"&&this.orientation==="vertical")this.range[f?"animate":"css"]({height:100-a+"%"},{queue:false,duration:e.animate})}}});b.extend(b.ui.slider,{version:"1.8.11"})})(jQuery);
(function(b,d){function e(){return++f}function g(){return++a}var f=0,a=0;b.widget("ui.tabs",{options:{add:null,ajaxOptions:null,cache:false,cookie:null,collapsible:false,disable:null,disabled:[],enable:null,event:"click",fx:null,idPrefix:"ui-tabs-",load:null,panelTemplate:"<div></div>",remove:null,select:null,show:null,spinner:"<em>Loading&#8230;</em>",tabTemplate:"<li><a href='#{href}'><span>#{label}</span></a></li>"},_create:function(){this._tabify(true)},_setOption:function(c,h){if(c=="selected")this.options.collapsible&&
h==this.options.selected||this.select(h);else{this.options[c]=h;this._tabify()}},_tabId:function(c){return c.title&&c.title.replace(/\s/g,"_").replace(/[^\w\u00c0-\uFFFF-]/g,"")||this.options.idPrefix+e()},_sanitizeSelector:function(c){return c.replace(/:/g,"\\:")},_cookie:function(){var c=this.cookie||(this.cookie=this.options.cookie.name||"ui-tabs-"+g());return b.cookie.apply(null,[c].concat(b.makeArray(arguments)))},_ui:function(c,h){return{tab:c,panel:h,index:this.anchors.index(c)}},_cleanup:function(){this.lis.filter(".ui-state-processing").removeClass("ui-state-processing").find("span:data(label.tabs)").each(function(){var c=
b(this);c.html(c.data("label.tabs")).removeData("label.tabs")})},_tabify:function(c){function h(r,u){r.css("display","");!b.support.opacity&&u.opacity&&r[0].style.removeAttribute("filter")}var i=this,j=this.options,n=/^#.+/;this.list=this.element.find("ol,ul").eq(0);this.lis=b(" > li:has(a[href])",this.list);this.anchors=this.lis.map(function(){return b("a",this)[0]});this.panels=b([]);this.anchors.each(function(r,u){var v=b(u).attr("href"),w=v.split("#")[0],y;if(w&&(w===location.toString().split("#")[0]||
(y=b("base")[0])&&w===y.href)){v=u.hash;u.href=v}if(n.test(v))i.panels=i.panels.add(i.element.find(i._sanitizeSelector(v)));else if(v&&v!=="#"){b.data(u,"href.tabs",v);b.data(u,"load.tabs",v.replace(/#.*$/,""));v=i._tabId(u);u.href="#"+v;u=i.element.find("#"+v);if(!u.length){u=b(j.panelTemplate).attr("id",v).addClass("ui-tabs-panel ui-widget-content ui-corner-bottom").insertAfter(i.panels[r-1]||i.list);u.data("destroy.tabs",true)}i.panels=i.panels.add(u)}else j.disabled.push(r)});if(c){this.element.addClass("ui-tabs ui-widget ui-widget-content ui-corner-all");
this.list.addClass("ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all");this.lis.addClass("ui-state-default ui-corner-top");this.panels.addClass("ui-tabs-panel ui-widget-content ui-corner-bottom");if(j.selected===d){location.hash&&this.anchors.each(function(r,u){if(u.hash==location.hash){j.selected=r;return false}});if(typeof j.selected!=="number"&&j.cookie)j.selected=parseInt(i._cookie(),10);if(typeof j.selected!=="number"&&this.lis.filter(".ui-tabs-selected").length)j.selected=
this.lis.index(this.lis.filter(".ui-tabs-selected"));j.selected=j.selected||(this.lis.length?0:-1)}else if(j.selected===null)j.selected=-1;j.selected=j.selected>=0&&this.anchors[j.selected]||j.selected<0?j.selected:0;j.disabled=b.unique(j.disabled.concat(b.map(this.lis.filter(".ui-state-disabled"),function(r){return i.lis.index(r)}))).sort();b.inArray(j.selected,j.disabled)!=-1&&j.disabled.splice(b.inArray(j.selected,j.disabled),1);this.panels.addClass("ui-tabs-hide");this.lis.removeClass("ui-tabs-selected ui-state-active");
if(j.selected>=0&&this.anchors.length){i.element.find(i._sanitizeSelector(i.anchors[j.selected].hash)).removeClass("ui-tabs-hide");this.lis.eq(j.selected).addClass("ui-tabs-selected ui-state-active");i.element.queue("tabs",function(){i._trigger("show",null,i._ui(i.anchors[j.selected],i.element.find(i._sanitizeSelector(i.anchors[j.selected].hash))[0]))});this.load(j.selected)}b(window).bind("unload",function(){i.lis.add(i.anchors).unbind(".tabs");i.lis=i.anchors=i.panels=null})}else j.selected=this.lis.index(this.lis.filter(".ui-tabs-selected"));
this.element[j.collapsible?"addClass":"removeClass"]("ui-tabs-collapsible");j.cookie&&this._cookie(j.selected,j.cookie);c=0;for(var p;p=this.lis[c];c++)b(p)[b.inArray(c,j.disabled)!=-1&&!b(p).hasClass("ui-tabs-selected")?"addClass":"removeClass"]("ui-state-disabled");j.cache===false&&this.anchors.removeData("cache.tabs");this.lis.add(this.anchors).unbind(".tabs");if(j.event!=="mouseover"){var l=function(r,u){u.is(":not(.ui-state-disabled)")&&u.addClass("ui-state-"+r)},k=function(r,u){u.removeClass("ui-state-"+
r)};this.lis.bind("mouseover.tabs",function(){l("hover",b(this))});this.lis.bind("mouseout.tabs",function(){k("hover",b(this))});this.anchors.bind("focus.tabs",function(){l("focus",b(this).closest("li"))});this.anchors.bind("blur.tabs",function(){k("focus",b(this).closest("li"))})}var m,o;if(j.fx)if(b.isArray(j.fx)){m=j.fx[0];o=j.fx[1]}else m=o=j.fx;var q=o?function(r,u){b(r).closest("li").addClass("ui-tabs-selected ui-state-active");u.hide().removeClass("ui-tabs-hide").animate(o,o.duration||"normal",
function(){h(u,o);i._trigger("show",null,i._ui(r,u[0]))})}:function(r,u){b(r).closest("li").addClass("ui-tabs-selected ui-state-active");u.removeClass("ui-tabs-hide");i._trigger("show",null,i._ui(r,u[0]))},s=m?function(r,u){u.animate(m,m.duration||"normal",function(){i.lis.removeClass("ui-tabs-selected ui-state-active");u.addClass("ui-tabs-hide");h(u,m);i.element.dequeue("tabs")})}:function(r,u){i.lis.removeClass("ui-tabs-selected ui-state-active");u.addClass("ui-tabs-hide");i.element.dequeue("tabs")};
this.anchors.bind(j.event+".tabs",function(){var r=this,u=b(r).closest("li"),v=i.panels.filter(":not(.ui-tabs-hide)"),w=i.element.find(i._sanitizeSelector(r.hash));if(u.hasClass("ui-tabs-selected")&&!j.collapsible||u.hasClass("ui-state-disabled")||u.hasClass("ui-state-processing")||i.panels.filter(":animated").length||i._trigger("select",null,i._ui(this,w[0]))===false){this.blur();return false}j.selected=i.anchors.index(this);i.abort();if(j.collapsible)if(u.hasClass("ui-tabs-selected")){j.selected=
-1;j.cookie&&i._cookie(j.selected,j.cookie);i.element.queue("tabs",function(){s(r,v)}).dequeue("tabs");this.blur();return false}else if(!v.length){j.cookie&&i._cookie(j.selected,j.cookie);i.element.queue("tabs",function(){q(r,w)});i.load(i.anchors.index(this));this.blur();return false}j.cookie&&i._cookie(j.selected,j.cookie);if(w.length){v.length&&i.element.queue("tabs",function(){s(r,v)});i.element.queue("tabs",function(){q(r,w)});i.load(i.anchors.index(this))}else throw"jQuery UI Tabs: Mismatching fragment identifier.";
b.browser.msie&&this.blur()});this.anchors.bind("click.tabs",function(){return false})},_getIndex:function(c){if(typeof c=="string")c=this.anchors.index(this.anchors.filter("[href$="+c+"]"));return c},destroy:function(){var c=this.options;this.abort();this.element.unbind(".tabs").removeClass("ui-tabs ui-widget ui-widget-content ui-corner-all ui-tabs-collapsible").removeData("tabs");this.list.removeClass("ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all");this.anchors.each(function(){var h=
b.data(this,"href.tabs");if(h)this.href=h;var i=b(this).unbind(".tabs");b.each(["href","load","cache"],function(j,n){i.removeData(n+".tabs")})});this.lis.unbind(".tabs").add(this.panels).each(function(){b.data(this,"destroy.tabs")?b(this).remove():b(this).removeClass("ui-state-default ui-corner-top ui-tabs-selected ui-state-active ui-state-hover ui-state-focus ui-state-disabled ui-tabs-panel ui-widget-content ui-corner-bottom ui-tabs-hide")});c.cookie&&this._cookie(null,c.cookie);return this},add:function(c,
h,i){if(i===d)i=this.anchors.length;var j=this,n=this.options;h=b(n.tabTemplate.replace(/#\{href\}/g,c).replace(/#\{label\}/g,h));c=!c.indexOf("#")?c.replace("#",""):this._tabId(b("a",h)[0]);h.addClass("ui-state-default ui-corner-top").data("destroy.tabs",true);var p=j.element.find("#"+c);p.length||(p=b(n.panelTemplate).attr("id",c).data("destroy.tabs",true));p.addClass("ui-tabs-panel ui-widget-content ui-corner-bottom ui-tabs-hide");if(i>=this.lis.length){h.appendTo(this.list);p.appendTo(this.list[0].parentNode)}else{h.insertBefore(this.lis[i]);
p.insertBefore(this.panels[i])}n.disabled=b.map(n.disabled,function(l){return l>=i?++l:l});this._tabify();if(this.anchors.length==1){n.selected=0;h.addClass("ui-tabs-selected ui-state-active");p.removeClass("ui-tabs-hide");this.element.queue("tabs",function(){j._trigger("show",null,j._ui(j.anchors[0],j.panels[0]))});this.load(0)}this._trigger("add",null,this._ui(this.anchors[i],this.panels[i]));return this},remove:function(c){c=this._getIndex(c);var h=this.options,i=this.lis.eq(c).remove(),j=this.panels.eq(c).remove();
if(i.hasClass("ui-tabs-selected")&&this.anchors.length>1)this.select(c+(c+1<this.anchors.length?1:-1));h.disabled=b.map(b.grep(h.disabled,function(n){return n!=c}),function(n){return n>=c?--n:n});this._tabify();this._trigger("remove",null,this._ui(i.find("a")[0],j[0]));return this},enable:function(c){c=this._getIndex(c);var h=this.options;if(b.inArray(c,h.disabled)!=-1){this.lis.eq(c).removeClass("ui-state-disabled");h.disabled=b.grep(h.disabled,function(i){return i!=c});this._trigger("enable",null,
this._ui(this.anchors[c],this.panels[c]));return this}},disable:function(c){c=this._getIndex(c);var h=this.options;if(c!=h.selected){this.lis.eq(c).addClass("ui-state-disabled");h.disabled.push(c);h.disabled.sort();this._trigger("disable",null,this._ui(this.anchors[c],this.panels[c]))}return this},select:function(c){c=this._getIndex(c);if(c==-1)if(this.options.collapsible&&this.options.selected!=-1)c=this.options.selected;else return this;this.anchors.eq(c).trigger(this.options.event+".tabs");return this},
load:function(c){c=this._getIndex(c);var h=this,i=this.options,j=this.anchors.eq(c)[0],n=b.data(j,"load.tabs");this.abort();if(!n||this.element.queue("tabs").length!==0&&b.data(j,"cache.tabs"))this.element.dequeue("tabs");else{this.lis.eq(c).addClass("ui-state-processing");if(i.spinner){var p=b("span",j);p.data("label.tabs",p.html()).html(i.spinner)}this.xhr=b.ajax(b.extend({},i.ajaxOptions,{url:n,success:function(l,k){h.element.find(h._sanitizeSelector(j.hash)).html(l);h._cleanup();i.cache&&b.data(j,
"cache.tabs",true);h._trigger("load",null,h._ui(h.anchors[c],h.panels[c]));try{i.ajaxOptions.success(l,k)}catch(m){}},error:function(l,k){h._cleanup();h._trigger("load",null,h._ui(h.anchors[c],h.panels[c]));try{i.ajaxOptions.error(l,k,c,j)}catch(m){}}}));h.element.dequeue("tabs");return this}},abort:function(){this.element.queue([]);this.panels.stop(false,true);this.element.queue("tabs",this.element.queue("tabs").splice(-2,2));if(this.xhr){this.xhr.abort();delete this.xhr}this._cleanup();return this},
url:function(c,h){this.anchors.eq(c).removeData("cache.tabs").data("load.tabs",h);return this},length:function(){return this.anchors.length}});b.extend(b.ui.tabs,{version:"1.8.11"});b.extend(b.ui.tabs.prototype,{rotation:null,rotate:function(c,h){var i=this,j=this.options,n=i._rotate||(i._rotate=function(p){clearTimeout(i.rotation);i.rotation=setTimeout(function(){var l=j.selected;i.select(++l<i.anchors.length?l:0)},c);p&&p.stopPropagation()});h=i._unrotate||(i._unrotate=!h?function(p){p.clientX&&
i.rotate(null)}:function(){t=j.selected;n()});if(c){this.element.bind("tabsshow",n);this.anchors.bind(j.event+".tabs",h);n()}else{clearTimeout(i.rotation);this.element.unbind("tabsshow",n);this.anchors.unbind(j.event+".tabs",h);delete this._rotate;delete this._unrotate}return this}})})(jQuery);

jQuery.fn.placeholder = function() 
{
	var counter=0;
	
	return this.each(function(){
		
		if ($(this).is("textarea"))
		{
			var placeholder = $(this).attr("placeholder");
			$(this).html(placeholder);
			
			$(this).css({color:'#999999',"font-style":"italic"});
			
			$(this).bind('focus', function(){
				if($(this).val()==placeholder)
				{
					$(this).val("");
					$(this).css({color:'inherit',"font-style":"normal"});
				}
			});
			
			$(this).bind('blur', function(){
                if($(this).val()==""){
					$(this).val(placeholder);
					$(this).css({color:'#999999',"font-style":"italic"});
				}
			});
		}
		else if ($(this).is("input")) {
			var id = $(this).attr("id");
			var tabindex = $(this).attr("tabindex");
			var placeholder = $(this).attr("placeholder");
			
			if($(this).attr("type")=="password")
			{
				var thisdummy = 'dummy' + counter;
				
				$(this).hide();
				$(this).after('<input type="text" id="' + thisdummy + '"/>');
				$('#' + thisdummy).val(placeholder);
				if (tabindex) $('#' + thisdummy).attr("tabIndex",tabindex);
				$('#' + thisdummy).css({color:'#999999',"font-style":"italic"});
				
				counter++;
				
				$('#' + thisdummy).bind('focus', function()
				{
					$("#" + id).show().val("");
					$("#" + id).show().focus();
					$(this).hide();
				}
				)
				
				$(this).bind('blur', function()
				{
					if($(this).val()=="")
					{
						$(this).hide();
						$("#" + thisdummy).show();
					};
				}
				)
			}
			
			if($(this).attr("type")=="text")
			{
				$(this).val(placeholder);
				$(this).css({color:'#999999',"font-style":"italic"});
				
				$(this).bind('focus', function()
				{
					if($(this).val()==placeholder)
					{
						$(this).val("");
						$(this).css({color:'inherit',"font-style":"normal"});
					}
				}
				)
				
				$(this).bind('blur', function()
				{
					if($(this).val()=="")
					{
						$(this).val(placeholder);
						$(this).css({color:'#999999',"font-style":"italic"});
					}
				}
				)
			}
		}
	});
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ajaxSend(function(event, xhr, settings) {
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


function helpUser(){
        if(typeof(user_id)!="undefined"){
            if($.cookies.get("new_user_"+user_id)!=null){
                //Obtenemos la sección actual
                var current_section=$('#right-col > div').attr('id')
                
                //Si hace falta creamos la cookie como un hash
                if($.cookies.get("new_user_"+user_id)=="")
                    $.cookies.set("new_user_"+user_id,{})
                
                var visited_sections=$.cookies.get("new_user_"+user_id);
                
                //Comprobamos si la sección no ha sido visitada
                if(typeof(visited_sections[current_section])=="undefined"){
                    visited_sections[current_section]=true;
                    $('.help-icon img').click();
                }
                
                //Marcamos la sección como visitada
                $.cookies.set("new_user_"+user_id,visited_sections)
            }
        }
    }


$(document).ready(function(){
    
    
            
    if($('.active-section').length!=0)
        $(".lavaLamp").lavaLamp({ fx: "backout", speed: 700 })
    $('.help-txt').dialog({
        autoOpen:false,
        resizable: false,
        buttons: [{
                text: "Cerrar",
                click: function() { $(this).dialog("close"); }
            }],
        draggable: false,
        width:560,
        position: ['center', 125]
    });



    
    $("[placeholder]").placeholder();
                
    $(".user-dropDownBtn, .user-submenu ").hoverIntent(hiConfig);
    $(".user-dropDownBtn").click(function(){
        //Alineamos el menu desplegable desde la esquina sup-izq.
        var tmp=$('#dropdown-list-user').width();
        tmp=52-tmp;
        $('#dropdown-list-user').css("margin-left",tmp+'px')
        
        $(this).find('ul:first:hidden').css({visibility: "visible",display: "none"}).slideDown(400);
    })
    
    /*** Resize right column ***/
    //$("#left-col").css("height",$(this).height()+'px');
    $("#right-col,#left-col").css("height","auto")
    //$("#right-col, #left-col").bind("resize",function(){
        
    //    if($("#right-col").height() > $("#left-col").height())
    //        $("#left-col").css("height",$("#right-col").height()+'px');
        //else
            //$("#right-col").css("height",$("#left-col").height()+'px');
    //});
    
    //$.bind("DOMSubtreeModified", function() {
    //    alert("tree changed");
    //});


    
    
    $('#search-form').bind('submit', function(e){
        e.preventDefault;
        window.location="/search/"+$(this).find("input[type='text']").val();
        return false;
    });


    var userAgent = navigator.userAgent.toLowerCase();
    jQuery.browser = {
        version: (userAgent.match( /.+(?:rv|it|ra|ie|me)[\/: ]([\d.]+)/ ) || [])[1],
        chrome: /chrome/.test( userAgent ),
        safari: /webkit/.test( userAgent ) && !/chrome/.test( userAgent ),
        opera: /opera/.test( userAgent ),
        msie: /msie/.test( userAgent ) && !/opera/.test( userAgent ),
        mozilla: /mozilla/.test( userAgent ) && !/(compatible|webkit)/.test( userAgent )
    };

    
    if($.browser.msie && $.browser.version.split(".")[0]!=9){
        $("body").children(":not('div#browser-error-msg,script#browser-error')").remove()
        $("#browser-error").tmpl({
            version:$.browser.version,
            browser: "Internet Explorer",
            download_url: "http://windows.microsoft.com/en-US/internet-explorer/products/ie/home"
        }).appendTo("body");
    }else if($.browser.mozilla && $.browser.version.split(".")[0]<3){
        $("body").children(":not('div#browser-error-msg,script#browser-error')").remove()
        $("#browser-error").tmpl({
            version:$.browser.version,
            browser: "Mozilla",
            download_url: "http://www.mozilla.org/es-ES/firefox/"
        }).appendTo("body");
    }else if($.browser.chrome && $.browser.version.split(".")[0]<11){
        $("body").children(":not('div#browser-error-msg,script#browser-error')").remove()
        $("#browser-error").tmpl({
            version:$.browser.version,
            browser: "Google Chrome",
            download_url: "http://www.google.es/chrome"
        }).appendTo("body");
    }else if($.browser.safari){
    }else if($.browser.opera){
    }
    
});

/*
 * jQuery resize event - v1.1 - 3/14/2010
 * http://benalman.com/projects/jquery-resize-plugin/
 * 
 * Copyright (c) 2010 "Cowboy" Ben Alman
 * Dual licensed under the MIT and GPL licenses.
 * http://benalman.com/about/license/
 */
(function($,h,c){var a=$([]),e=$.resize=$.extend($.resize,{}),i,k="setTimeout",j="resize",d=j+"-special-event",b="delay",f="throttleWindow";e[b]=250;e[f]=true;$.event.special[j]={setup:function(){if(!e[f]&&this[k]){return false}var l=$(this);a=a.add(l);$.data(this,d,{w:l.width(),h:l.height()});if(a.length===1){g()}},teardown:function(){if(!e[f]&&this[k]){return false}var l=$(this);a=a.not(l);l.removeData(d);if(!a.length){clearTimeout(i)}},add:function(l){if(!e[f]&&this[k]){return false}var n;function m(s,o,p){var q=$(this),r=$.data(this,d);r.w=o!==c?o:q.width();r.h=p!==c?p:q.height();n.apply(this,arguments)}if($.isFunction(l)){n=l;return m}else{n=l.handler;l.handler=m}}};function g(){i=h[k](function(){a.each(function(){var n=$(this),m=n.width(),l=n.height(),o=$.data(this,d);if(m!==o.w||l!==o.h){n.trigger(j,[o.w=m,o.h=l])}});g()},e[b])}})(jQuery,this);
/**
* hoverIntent r6 // 2011.02.26 // jQuery 1.5.1+
* <http://cherne.net/brian/resources/jquery.hoverIntent.html>
* 
* @param  f  onMouseOver function || An object with configuration options
* @param  g  onMouseOut function  || Nothing (use configuration options object)
* @author    Brian Cherne brian(at)cherne(dot)net
*/
(function($){$.fn.hoverIntent=function(f,g){var cfg={sensitivity:7,interval:100,timeout:0};cfg=$.extend(cfg,g?{over:f,out:g}:f);var cX,cY,pX,pY;var track=function(ev){cX=ev.pageX;cY=ev.pageY};var compare=function(ev,ob){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);if((Math.abs(pX-cX)+Math.abs(pY-cY))<cfg.sensitivity){$(ob).unbind("mousemove",track);ob.hoverIntent_s=1;return cfg.over.apply(ob,[ev])}else{pX=cX;pY=cY;ob.hoverIntent_t=setTimeout(function(){compare(ev,ob)},cfg.interval)}};var delay=function(ev,ob){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);ob.hoverIntent_s=0;return cfg.out.apply(ob,[ev])};var handleHover=function(e){var ev=jQuery.extend({},e);var ob=this;if(ob.hoverIntent_t){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t)}if(e.type=="mouseenter"){pX=ev.pageX;pY=ev.pageY;$(ob).bind("mousemove",track);if(ob.hoverIntent_s!=1){ob.hoverIntent_t=setTimeout(function(){compare(ev,ob)},cfg.interval)}}else{$(ob).unbind("mousemove",track);if(ob.hoverIntent_s==1){ob.hoverIntent_t=setTimeout(function(){delay(ev,ob)},cfg.timeout)}}};return this.bind('mouseenter',handleHover).bind('mouseleave',handleHover)}})(jQuery);
// Defino que submenus deben estar visibles cuando se pasa el mouse por encima            
hiConfig = {
    sensitivity: 2, // number = sensitivity threshold (must be 1 or higher)
    interval: 0, // number = milliseconds for onMouseOver polling interval
    timeout: 500, // number = milliseconds delay before onMouseOut
    over: function() {
        $(this).find('ul:first:hidden').css({visibility: "visible",display: "none"}).slideDown(400);
    },
    out: function() {
        
        var inputVisibility=$('#dropdown-list .new-list').css('display');
        if($("#dropdown-list").hasClass('visible-display')==false && inputVisibility!="inline-block"){
            $(this).find('ul:first').slideUp(400);
            $("#dropdown-list").removeClass('visible-display');
            
        }
        
    }
}

GRM = { common : {}, autocomplete : {} };

GRM.common.token = "*****GRMtoken****";

GRM.common.extend = function(m, e){
    var e = e || this;
    for (var x in m) e[x] = m[x];
    return e;
};

GRM.common.get = function(s){
    if (typeof(s) == "string")
        return $(s);
    
    return s;
};

/*
    <span class="like-dislike" value="{{obj.instance.id}}" {% if obj.has_voted %}like="true"{%endif%} type="suggestion">
        <span class="dislike">
            <span class="hoverlink">Ya no me gusta</span> 
            <span class="text like-text increase">{{obj.vote_counter}}</span> personas
        </span>

        <span class="like">
            Me gusta
        </span>
    </span>
    
    $('.like-dislike').like({like_class: "xxx", dislike_class: "xxx", progress_class: "xxx"});
*/
GRM.like = function(settings) {
    
    settings = jQuery.extend({
        like_class: null,
        dislike_class: null,
        progress_class: null,
        callback: null           
    }, settings);
    
    var token = "grm-like";
    
    return this.each(function(){
        
        if ($(this).attr(token))
            return;
        $(this).attr(token,true);

        // get init state
        var state = (typeof $(this).attr('like') != "undefined" );

        // auto-init classes
        if (state && settings.dislike_class)
            $(this).addClass(settings.dislike_class);
        if (!state && settings.like_class)
            $(this).addClass(settings.like_class);

        // auto-init show/hide
        if (state)
            $(this).find('.like').hide();
        else
            $(this).find('.dislike').hide();


        // counter incremental
        /*var inc = $(this).find('.increase');
        $.each(inc, function(index,item){
            $(item).text(parseInt($(item).text())+1);
        });*/
        
        $(this).click(function() {
            
            
            var type = $(this).attr('type'), id = $(this).attr('value'), vote = (typeof $(this).attr('like') != "undefined" )?-1:1;
            
            /*GRM.wait();
            if (settings.progress_class)
                $(this).addClass(settings.progress_class);*/
            
            function toggleme(me) {
                // disliking
                if (typeof me.attr('like') != "undefined") {
                    // send vote -1
                    me.find('.dislike').hide();
                    me.find('.like').show();
                    me.removeAttr("like");
                    
                    if (settings.dislike_class)
                        me.removeClass(settings.dislike_class);
                    
                    if (settings.like_class)
                        me.addClass(settings.like_class);
                        
                }
                
                // liking
                else {
                    // send vote +1
                    me.find('.like').hide();
                    me.find('.dislike').show();
                    me.attr("like","true");
                    
                    if (settings.like_class)
                        me.removeClass(settings.like_class);
                    
                    if (settings.dislike_class)
                        me.addClass(settings.dislike_class);
                }
                
            }
            
            toggleme($(this));
            
            $.ajax({
                    type: "POST",
                    url: "/ajax/vote/"+type+"/",
                    data: {
                        instance_id:id,
                        puntuation: vote
                    },
                    context: $(this),
                    error: function() { toggleme($(this)); },
                    success: function(data){
                        
                        if(data!=null)
                            $(this).find('.increase').text(data.votes);
                        else {
                            showMessage("Pio! Perdona se ha producido un error<br>Estamos trabajando en solucionarlo","error");
                            toggleme($(this));
                        }
                        
                        if (settings.callback)
                            settings.callback();
                        
                    },
                    complete: function()
                    {
                        /*
                        if (settings.progress_class)
                            $(this).removeClass(settings.progress_class);
                        GRM.nowait();*/
                    }
                });
        });
    });
};

/*
    <span title="Guardar en favoritos"  class="remember-forget" value="{{obj.instance.id}}" {%if obj.user_follower%}remember="true"{%endif%}>
        <span class="remember">Guardar</span>
        <span class="forget">Guardado</span>
    </span>
    
    $('.remember-forget').remember({remember_class: "xxx", forget_class: "xxx", progress_class: "xxx"});
*/
GRM.remember = function(settings) {
    
    settings = jQuery.extend({
        remember_class: null,
        forget_class: null,
        progress_class: null,
        callback: null    
    }, settings);
    
    var token = "grm-remember";
    
    return this.each(function(){
        
        if ($(this).attr(token))
            return;
        $(this).attr(token,true);
        
        // get init state
        var state = (typeof $(this).attr('remember') != "undefined" );

        // auto-init classes
        if (state && settings.forget_class)
            $(this).addClass(settings.forget_class);
        if (!state && settings.remember_class)
            $(this).addClass(settings.remember_class);

        // auto-init show/hide
        if (state)
            $(this).find('.remember').hide();
        else
            $(this).find('.forget').hide();

        $(this).click(function() {
            
            
            //Primero comprobamos el tipo de mensaje
            var elemType;
            if ($(this).attr('type')=="list")
                elemType="list";
            else
                elemType="suggestion";
            var id = $(this).attr('value'), url = (typeof $(this).attr('remember') != "undefined" )?"/ajax/delete/"+elemType+"/follower/":"/ajax/add/"+elemType+"/follower/";
            
            
            /*
            GRM.wait();
            if (settings.progress_class)
                $(this).addClass(settings.progress_class);*/


            function toggleme(me) {
                // disliking
                if (typeof me.attr('remember') != "undefined" ) {
                    // send vote -1
                    me.find('.forget').hide();
                    me.find('.remember').show();
                    me.removeAttr("remember");
                    
                    if (settings.forget_class)
                        me.removeClass(settings.forget_class);
                    
                    if (settings.remember_class)
                        me.addClass(settings.remember_class);
                        
                }
                
                // liking
                else {
                    // send vote +1
                    me.find('.remember').hide();
                    me.find('.forget').show();
                    me.attr("remember","true");
                    
                    if (settings.remember_class)
                        me.removeClass(settings.remember_class);
                    
                    if (settings.forget_class)
                        me.addClass(settings.forget_class);
                    }
                
                }
            
            toggleme($(this));
            
            $.ajax({
                    type: "POST",
                    url: url,
                    data: {
                        eventid:id,
                        list_id:id
                    },
                    context: $(this),
                    error: function() {
                        toggleme($(this));
                    },
                    success: function(){
                        
                        if (settings.callback)
                            settings.callback();
                    },
                    complete: function()
                    {
                        /*if (settings.progress_class)
                            $(this).removeClass(settings.progress_class);
                        GRM.nowait();*/
                    }
                });
        });
    });
};

/*
    HOW TO USE
    --------------------------------
    HTML Template needed:
    
    <span class="btn dropDownBtn">
        Guardar en
        <ul class="submenu" style="display:none" id="dropdown-list">
            {% if lists %}
                {% for obj in lists %}
                    {% if obj.user.username = request.user.username %}
                        <!-- Solo se muestran mis listas -->
                        <li id="listid-{{obj.id}}">{{obj.name}} (<span class="list-{{obj.id}}-counter">{{obj.keys|length}}</span> sugerencias)</li>
                    {% endif %}
                {% endfor %}
            {% endif %}
            <li class="new-list-btn">
                <span id="text">Nueva lista...</span>
                <span class="new-list" style="display:none"><input type="text" /></span><div id="cancel-link" onclick="closeDropdown()" style="display:none">Cancel</div>
            </li>
        </ul>
    </span>
    
    Javascript call at onready
    $('.dropDownBtn').menuList({onNewList: function(){}});
*/
GRM.menuList = function(settings) {
    
    settings = jQuery.extend({
        onNewList: null,
        onLiClick: null
        
    }, settings);
       
    return this.each(function(){
        
        // Menu desplegable "Listas"
            
            
            $(this).hoverIntent(hiConfig);
            $(this).find('.submenu').hoverIntent(hiConfig);
            $(this).click(function(){
                $(this).find('ul:first:hidden').css({visibility: "visible",display: "none"}).slideDown(400);
            })
            
            //console.log("settings.onLiClick="+settings.onLiClick)
            if(settings.onLiClick!=null)
                $(this).find('.submenu li:not(.dropDownBtn-btn,.new-list-btn)').click(settings.onLiClick);
            else
                $(this).find('.submenu li:not(.dropDownBtn-btn,.new-list-btn)').click(function(){submenuLiBehave(this)})
            
            //Enter behave when adding new list on Suggestions Tab
            $(this).find(".new-list-btn span.new-list").keyup(function(e) {
                var suggestionList=[];
                e.preventDefault();
                if (e.which == 27){
                    //On press escape
                    closeDropdown();
                }else if(e.keyCode == 13) {
                    if(settings.onNewList!=null){
                        settings.onNewList($(this).find('input').val());
                    }else{
                        //On press enter
                        //Comprobamos si hay sugerencias seleccionadas para añadirlas
                        var checkedSuggestions=$('.suggestion input[name=suggestions]').filter(':checked');
                        if( checkedSuggestions.length>0){
                            checkedSuggestions.each(function(){
                                suggestionList.push($(this).attr('id').substring(9,$(this).attr('id').length))
                            })
                        }
                        
                        $.ajax({
                            type: "POST",
                            url: url["modify_suggestion_list"],
                            data: {
                                name: $(this).find('input').val(),
                                suggestions: suggestionList
                            },
                            dataType:'json',
                            success: function(data){
                                //Añadimos la lista al desplegable
                                $("<li id=\"listid-"+data.id+"\">"+data.name+" (<span class=\"list-"+data.id+"-counter\">"+data.keys.length+"</span> sugerencias)</li>").insertBefore('.new-list-btn');
                                $('#listid-'+data.id).click(function(){submenuLiBehave(this)});
                                
                                //Añadimos la lista en la pestaña listas
                                
                                //Reordenamos alfabéticamente la lista desplegable
                                $('.submenu li').not('li.new-list-btn').sortElements(function(a, b){
                                    return $(a).text().toLowerCase() > $(b).text().toLowerCase() ? 1 : -1;
                                });
                                
                                $("#dropdown-list").removeClass('visible-display');
                                
                                //Añadimos a la sugerencia dentro de la lista de sugerencias 
                                //las nuevas listas en las que se encuentra
                                updateSuggestions(data);
                                
                                //Actualizamos el contador de la lista con el número de sugerencias
                                updateCounter(data.id,data.keys.length);
                                
                                //Añadimos la lista a la pestaña listas
                                var suggestions=[];
                                $(data.keys).each(function(){
                                    suggestions.push({
                                            id:this,
                                            name:$('#suggestion_'+this+' .suggestionName_editable').text()
                                        })
                                })
                                var obj=$("#listTemplate").tmpl({obj:data, keys:suggestions}).appendTo("#suggestion-list-lists");
                                if(obj.find('.suggestions ul li').length > 0){
                                    tmp=obj;
                                    obj.find('.suggestions ul').show();
                                    obj.find('.suggestions .empty-msg').hide();
                                    obj.find('.suggestions li.removable').click(function(){
                                        var unparsedString=$(this).attr('class').split(" ")[0];
                                        var listID = unparsedString.substring(5,unparsedString.length)
                                        removeFromList(this,listID);
                                    });
                                }
                                
                                
                                setExpandible('#list_'+data.id);
                                
                                
                                // Activamos el mismo comportamiento que tienen el resto de listas:
                                // que se puedan editar los campos, que se activen los diálogos para compartir
                                // y que se puedan mostrar y ocultar las estadísticas
                                set_editable_fields();
                                
                                create_share_links();
                                
                                obj.find('.show-more').click(show_and_hide_stats_callback);
                                
                                //Aumentamos el contador de las listas
                                $('#lists-tab-counter').text(parseInt($('#lists-tab-counter').text())+1);
                                
                                //Mostrar mensaje de éxito
                                showMessage("La lista ha sido añadida con éxito","success")
                                
                                
                            }
                        });
                    }
                    
                        
                    
                    $(".new-list-btn span#text").css('display','inline-block')
                    $(".new-list-btn span.new-list").css('display','none')
                    $(".new-list-btn div#cancel-link").css('display','none')
                    $(".new-list-btn span.new-list").find('input').val("");
                }                
            });
            
            //Reordenamos alfabéticamente la lista desplegable
            $('.submenu li').not('li.new-list-btn').sortElements(function(a, b){
                return $(a).text().toLowerCase() > $(b).text().toLowerCase() ? 1 : -1;
            });
            
            //Convierte el texto de nueva lista en un input field
            $(this).find('.new-list-btn span#text').click(function(){                
                $(this).css('display','none')
                $(this).parent().find("span.new-list").css('display','inline-block')
                $(this).parent().find("span.new-list").find('input').focus()
                $(this).parent().find("div#cancel-link").css('display','block')
                var tmp=$('#text').parentsUntil('.dropDownBtn');
                var dropdown=tmp[tmp.length-1]
                $(dropdown).addClass('visible-display');
            })
        
    });
}

GRM.removable = function() {

    var token = "grm-removable";

    return this.each(function(){

        if ($(this).attr(token))
            return;
        $(this).attr(token,true);

        $(this).hide();
        
        var item = $(this);
        
        
        $(this).parent().hover(
            
            function(){item.show();},
            function(){item.hide();}
        );

        $(this).click(function(){
            var id = $(this).attr('value'), type = $(this).attr('type');
            
            var custom_url;
            if(type=="person")
                custom_url="/ajax/contacts/block/";
            else
                custom_url="/ajax/delete/"+type+"/";
            
            var data = { eventid:id,  comment_id:id, list_id:id, userid:id};
            GRM.wait();
            $.ajax({
                type: "POST",
                url: custom_url,
                data: data,
                dataType:'json',
                context:$(this),
                complete: function() { GRM.nowait();},
                success: function(msg){
                    
                    if(msg==true){

                        if (type=="comment"){
                            //Eliminamos el comentario
                            var preElem=$(this).parent().prev();
                            var posElem=$(this).parent().next();
                            //parentTree=elem.parentsUntil('.suggestion-element');
                            if(preElem.size()==0 && posElem.size()==0){
                                //Si al borrar el comentario ya no quedan más elementos
                                //Ocultamos la caja de comentarios
                                $(this).parent().parent().next().addClass('hidden');
                                
                            }
                            
                            $(this).parent().fadeOut('slow').remove();
                            
                        }else if(type=="suggestion" || type=="suggestion/list" || type=="person")
                            $(this).parent().parent().fadeOut('slow').remove()
                        
                        //Si estamos en chronology actualizamos los contadores de los tabs
                        if($('ul#chronology').length>0)
                            GRM.updateTabCounters();
                    
                            
                    }
                },
                error:function(){
                }
                
            });
        });

    });

}

GRM.loadPage = function(params){
    
            var page=params['page'];
            var container=params['container'];
            var url=params['url'];
            var template=params['template'];
            var data=params["data"];
            var total=params["total_pages"];
            var current_page = ( typeof $(container).attr('page') == 'undefined' )?1:parseInt($(container).attr('page'));
            
            if (page=='next')
                current_page++;
            else if(page=='prev' && current_page>1)
                current_page--;

            data['page'] = current_page;
            
            $.ajax({
                type: 'POST',
                url: url,
                data:data,
                success: function(data){
                    
                    $(container).attr("page",current_page);
                    
                    //$(container).empty();
                    $.each(data[1], function(index,suggestion){
                        $(template).tmpl( {element:suggestion} ).appendTo(container);
                    });

                    //Ocultamos los botones de siguiente y anterior si es necesario
                    if(current_page>1)
                        $('#prev-page').removeClass('hidden');
                    else
                        $('#prev-page').addClass('hidden');
                        
                    if(current_page<total)
                        $('#next-page').removeClass('hidden');
                    else
                        $('#next-page').addClass('hidden');
                }
            });
        }

GRM.loadTimeline = function(settings){

        var token = "grm-loadtimeline";

        settings = jQuery.extend({
            container: null
            
        }, settings);
           
        return this.each(function(){
            
                    if ($(this).attr(token))
                        return;
                        
                    $(this).attr(token,true);
                    
                    $(this).click(function(){
                        
                    var loadmore = $(this);
                    
                    var data = {};
                    data['query_id'] = $(settings.container).attr("value");
                    
                    if ($(settings.container).attr("username"))
                        data['username'] = $(settings.container).attr("username");
                    
                    loadmore.addClass("waiting");

                    var url = '/ajax/get/'+$(this).attr('type')+'/';
                    
                    $.ajax({
                        type: 'POST',
                        url: url,
                        data: data,
                        complete: function() { loadmore.removeClass("waiting"); },
                        success: function(data){
                            if(data[1].length>0){
                                if(data[0].length==2)
                                    $(settings.container).attr("value",'["'+data[0][0]+'","'+data[0][1]+'"]');
                                else
                                    $(settings.container).attr("value",data[0]);
                                var nextPage=parseInt($(settings.container).attr("page"))+1;
                                $(settings.container).attr("page",nextPage);
                                
                                $.each(data[1], function(index,suggestion){
                                    var temp=$(suggestion).appendTo(settings.container);
                                    //Anadimos el valor de la página para añadir comportamientos
                                    $(temp).first().attr('value',nextPage);
                                });
                                
                                setTimelineBehaviour(nextPage);
                                
                                GRM.updateTabCounters();
                                
                                //Volvemos a filtrar la pestaña activa forzando evento click
                                $('#'+$('ul#tabMenu .active').attr('id')).click()
                                
                                
                            }
                            showMessage("Se han cargado "+data[1].length+" elementos nuevos","success");
                            if(data[1].length<10){
                                //Si no hay más datos ocultamos el boton de cargar más
                                loadmore.hide();
                            }
                        }
                    });
                });
        });
    }

GRM.sendComment = function(type,text,id,callback){
    
    if(text=="")
        return false;

    GRM.wait();

    $.ajax({
        type: "POST",
        url: "/ajax/add/comment/"+type+"/",
        data: {
            instance_id:id,
            msg:text },
        dataType:'json',
        complete: function() { GRM.nowait(); },
        success: function(response){
            
            var message=$('#msg').val()
            $('#msg').val("")
            
            var c = $('#commentTemplate').tmpl(response).prependTo('#comment-list');
            
        
            c.find(".like-dislike").like();
            c.find(".removable").removable();
            //if (typeof resizeIframe != "undefined") resizeIframe();
            
            showMessage("El comentario ha sido añadido con éxito", "success")
            
            if (typeof callback != "undefined")
                callback();
        }
    });

    return true;
}

GRM.updateTabCounters = function(){
    //~ $('#all-counter').text('('+$('#chronology li').not('.comment-box li').length+')');
    $('#suggestions-counter').text('('+$(':regex(class,(msg-300|msg-303))').length+')');
    $('#lists-counter').text('('+$(':regex(class,(msg-350|msg-353))').length+')');
    $('#likes-counter').text('('+$(':regex(class,(msg-125|msg-305|msg-355))').length+')');
    $('#comments-counter').text('('+$(':regex(class,(msg-120|msg-121))').length+')');
}

GRM.wait = function() {
    if ($("#wait-mask").size()==0) {
        $("body").append("<div id='wait-mask' style='position:fixed;height:100%;width:100%;top:0px;left:0px;z-index:1000;cursor:wait;'></div>");
        }
    else {
        $("#wait-mask").show();
    }
}

GRM.nowait = function() {
    $("#wait-mask").hide();
}

GRM.search = function(str,containers,fields)
{    
    var words = [];
    var rawwords = str.split(' ');
    
    for (var i in rawwords)
    {
        if (typeof(rawwords[i])=="string" && rawwords[i] != '' && words.indexOf(rawwords[i])<0)
            words.push(rawwords[i]);
        
    }
    
    $(containers+" .expanded").hide();
    
    // no words entered
    if (words.length==0)
    {
        $(containers).not(".expanded").show();
    }
    else
    {        
        var regexp=new RegExp("("+words.join('|')+")","im");
        
        $.each($(containers),function(idx,item) {
            item = $(item);
            item.hide();
            for (var i=0;i<fields.length;i++) {
                    if (item.find(fields[i]).text().search(regexp)>=0) {
                            var id = "#"+item.attr('id');
                            $(id+","+id+' > *').not(".expanded").show();
                            break;
                        }
                }
            
            });
    }
}

GRM.common.checkemail = function(email) {
	var regexp  = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	
	return (regexp.test(email));				
}

GRM.autocomplete.frompoint = function() {
    
    }

GRM.autocomplete.topoint = function() {
    
    }

jQuery.fn.search = function(container,fields) {
    return this.each(function(){
        $(this).keyup(function(){GRM.search($(this).val(),  container, fields)});
    });
}

jQuery.fn.like = GRM.like;
jQuery.fn.loadTimeline = GRM.loadTimeline;
jQuery.fn.remember = GRM.remember;
jQuery.fn.removable = GRM.removable;
jQuery.fn.menuList = GRM.menuList;

GRM.init = function() {
        $(".like-dislike").like();
        $(".remember-forget").remember();
        $(".removable").removable();
    }

//$(document).ready(GRM.init);

jQuery.expr[':'].regex = function(elem, index, match) {
    var matchParams = match[3].split(','),
        validLabels = /^(data|css):/,
        attr = {
            method: matchParams[0].match(validLabels) ?
                        matchParams[0].split(':')[0] : 'attr',
            property: matchParams.shift().replace(validLabels,'')
        },
        regexFlags = 'ig',
        regex = new RegExp(matchParams.join('').replace(/^\s+|\s+$/g,''), regexFlags);
    return regex.test(jQuery(elem)[attr.method](attr.property));
}


function sendComment(btn,elemType,id) {
    if (GRM.sendComment(elemType,$('#msg').val(),id,function(){$(btn).text("Comentar");$(btn).removeClass("waiting");})){
        $(btn).text("Enviando")
        $(btn).addClass("waiting")
    }
}

function showMessage(txt,msgClass){
    if($('#notification-msg').css("display")=="none"){
        $('#notification-msg').attr('class',"")
        $('#notification-msg').html(txt)
        $('#notification-msg').addClass(msgClass)
        var posTop=$(window).scrollTop();
        if(posTop<60)posTop=60;
        $('#notification-msg').css('top',posTop+'px');
        $('#notification-msg').fadeIn('slow').delay(3000).fadeOut('slow')
    }
}
'#id_name','#counter'
function setRemainingCharCounter(input,counter){
    $(input).keyup(function(){
        charLeft=140-$(input).val().length;
        $(counter).text(charLeft);
        if(charLeft<0)
            $(counter).css("color","red")
        if(charLeft>-1)
            $(counter).css("color","#777")
        
    })
    
    //$('#id_name').trigger('keyup');
}

//Cierra el menu desplegable
function closeDropdown(){
    $("#dropdown-list").removeClass('visible-display');
    $(".new-list-btn span#text").css('display','inline-block');
    $(".new-list-btn span.new-list").css('display','none');
    $(".new-list-btn div#cancel-link").css('display','none');
    $(".new-list-btn span.new-list").find('input').val("");
}

function FormatNumberLength(num, length) {
    var r = "" + num;
    while (r.length < length) {
        r = "0" + r;
    }
    return r;
}

function validateDates(start,end){
    //Date format mm/dd/aaaa
    var start = start.split("/");
    var end = end.split("/");
    
    start = new Date(start[0], start[1] -1, start[2]);
    end = new Date(end[0], end[1] -1, end[2]);

    if (start > end) 
        return false;
    else
        return true;
}
function validateTimes(start,end){
    //Time format hh:mm
    var start = start.split(":");
    var end = end.split(":");
    
    if(start[0]>end[0])
        return false;
    else if(start[0]==end[0] && start[1]>end[1])
        return false;
    return true;
}

function checkEmail() {
    var email = $('#registerEmail').val();
    var item = $('#registerEmail').next('div');
    var st = $('#emailStatus');
    item.text('');
    st.hide();

    if (email=='Email') {
        item.text('Necesitamos que rellenes el email');
        //$(email).addClass('error');
        item.show();
        st.removeClass("ok").addClass("no-ok");
        st.show();
        return false;
    }
    
    if (!GRM.common.checkemail(email)) {
        item.text('E-mail inválido');
        item.show();
        st.removeClass("ok").addClass("no-ok");
        st.show();
        return false;
    }
    else {
        $.ajax({
            url:"/ajax/exists/",
            type:'post',
            dataType:'json',
            data: {
                email: email,
                "csrfmiddlewaretoken": $('#registerFormForm input[type="hidden"]').val() 
            },
            async:true,
            success: function(data){ 
        
                if(data.result){
                    item.text("Esta cuenta ya está siendo usada");
                    item.show();
                    st.removeClass("ok").addClass("no-ok");
                    st.show();
                }
                else
                {
                    //item.text("Esta cuenta ya está siendo usada");
                    st.removeClass("no-ok").addClass("ok");
                    st.show();
                    item.hide();
                }
            }
        });
    }
    
    return true;
}

function checkTerms() {
    if (!$('#termsCheckbox').is(":checked")) {
       showMessage("Para poder crear una cuenta primero necesitas leer y aceptar las condiciones de uso.","error");
       return false;
    }
    return true;
}

function checkPasswords(emptymessage) {
    
    var pwd1 = $('#userRegisterPass1').val(), pwd2 = $('#userRegisterPass2').val();
    var item = $('#passwordStatus');
    
    if (pwd1.length==0 || pwd2.length==0) {

        if (emptymessage) {
            item.text("Debes rellenar los dos campos de las contraseñas");
            item.show();
        }

        return false;
        }
    
    if (pwd1!=pwd2){

        item.text("Las contraseñas no coinciden, por favor vuelva a introducirlas");
        item.show();

        return false;
        }
    
    if (pwd1.length<6){
        item.text("La contraseña tiene que tener al menos 6 caracteres");
        item.show();
        return false;
        }
    
    return true;
}

function showMenu(){
    $('#login-bar p').show();
    $('#login-bar ul').show();
    $('#georemindme-form').hide();
}

function checkUncheck(obj){
    var checkbox=$(obj).find('input');
    if($(checkbox).attr('checked')==true)
        $(checkbox).attr('checked',false);
    else
        $(checkbox).attr('checked',true)
}

/**
 * jQuery.fn.sortElements
 * --------------
 * @param Function comparator:
 *   Exactly the same behaviour as [1,2,3].sort(comparator)
 *   
 * @param Function getSortable
 *   A function that should return the element that is
 *   to be sorted. The comparator will run on the
 *   current collection, but you may want the actual
 *   resulting sort to occur on a parent or another
 *   associated element.
 *   
 *   E.g. $('td').sortElements(comparator, function(){
 *      return this.parentNode; 
 *   })
 *   
 *   The <td>'s parent (<tr>) will be sorted instead
 *   of the <td> itself.
 */
jQuery.fn.sortElements = (function(){
 
    var sort = [].sort;
 
    return function(comparator, getSortable) {
 
        getSortable = getSortable || function(){return this;};
 
        var placements = this.map(function(){
 
            var sortElement = getSortable.call(this),
                parentNode = sortElement.parentNode,
 
                // Since the element itself will change position, we have
                // to have some way of storing its original position in
                // the DOM. The easiest way is to have a 'flag' node:
                nextSibling = parentNode.insertBefore(
                    document.createTextNode(''),
                    sortElement.nextSibling
                );
 
            return function() {
 
                if (parentNode === this) {
                    throw new Error(
                        "You can't sort elements if any one is a descendant of another."
                    );
                }
 
                // Insert before flag:
                parentNode.insertBefore(this, nextSibling);
                // Remove flag:
                parentNode.removeChild(nextSibling);
 
            };
 
        });
 
        return sort.call(this, comparator).each(function(i){
            placements[i].call(getSortable.call(this));
        });
 
    };
 
})();  


(function($){  
$.extend(  
{  
    jsonp: {  
        script: null,  
        options: {},  
        call: function(url, options) {  
            var default_options = {  
                callback: function(){},  
                callbackParamName: "callback",  
                params: []  
            };  
            this.options = $.extend(default_options, options);  
            //Determina si se debe añadir el parámetro separado por ? o por &  
            var separator = url.indexOf("?") > -1? "&" : "?";  
            var head = $("head")[0];  
            /*Serializa el objeto en una cadena de texto con formato URL*/  
            var params = [];  
            for(var prop in this.options.params){  
                params.push(prop + "=" + encodeURIComponent(options.params[prop]));  
            }  
            var stringParams = params.join("&");  
            //Crea el script o borra el usado anteriormente  
            if(this.script){  
                head.removeChild(script);  
            }  
            script = document.createElement("script");  
            script.type = "text/javascript";  
            //Añade y carga el script, indicandole que llame al metodo process  
            script.src = url + separator + stringParams + (stringParams?"&":"") + this.options.callbackParamName +"=jQuery.jsonp.process";  
            head.appendChild(script);  
        },  
        process: function(data) { this.options.callback(data); }  
    }  
});  
})(jQuery)  

//How to use: showHelp('#mobile','#texto3','right');
function showHelp(element,text_help,position,plusLeft,plusTop){
	if(!$(text_help).hasClass('help-box'))
		$(text_help).addClass('help-box');
	
	$(text_help +' div.arrow').each(function(i,elem){
		$(elem).remove();
	});
	arrow = $('<div class="arrow arrow-'+position+'"></div>');
	$(text_help).append(arrow);
	

	var adjust_top,adjust_left,arrow_top,arrow_left;
	var box_size = [$(text_help).width(),$(text_help).height()]
	
	if(position==='right'){
		adjust_top=-15;
		adjust_left=-300;
		arrow_top=0;
		arrow_left=box_size[0]+11;//5px porque tiene 10 de ancho
	}else if(position==='left'){
		adjust_top=-15;
		adjust_left=$(element).width();
		arrow_top=0;
		arrow_left=-11;//5px porque tiene 10 de ancho
	}else if(position==='up'){
		adjust_top=$(element).height();
		adjust_left=-$(text_help).width()/2+$(element).width()/2-20;
		arrow_top=-11;
		arrow_left=box_size[0]/2-5;//5px porque tiene 10 de ancho
	}else if(position==='down'){
		adjust_top=-$(text_help).height()-40;
		adjust_left=-$(text_help).width()/2+$(element).width()/2-20;
		arrow_top=box_size[1]+8;
		arrow_left=box_size[0]/2-5;//5px porque tiene 10 de ancho
	}

	if(plusTop!=null)
		adjust_top += plusTop;
	if(plusLeft!=null)
		adjust_left += plusLeft;

	
	var pos=$(element).position()
	var top_pos=pos['top']+adjust_top;
	var left_pos=pos['left']+adjust_left;
	
	$(text_help).css('top',top_pos+'px')
	$(text_help).css('left',left_pos+'px')
	
	$(text_help).show();
	
	$(text_help +' div.arrow').css('top',arrow_top+'px')
	$(text_help +' div.arrow').css('left',arrow_left+'px')
	
	if($('#showing-help').length==0){
		invisible_layer = $('<div id="showing-help" style="width:100%;height:100%;position:absolute;z-index:99" onclick="javascript:closeHelp()"></div>');
		$('body').prepend(invisible_layer)
	}
}

function closeHelp(){
	$('.help-box').hide();
	$('#showing-help').remove();
}

// ensuring ajax https
$(document).ajaxSend(function(event, xhr, settings) {
    if ( document.location.hostname != "localhost" && document.location.hostname != "127.0.0.1" && document.location.protocol.slice(0,5) != "https" && settings.url.slice(0,6)=="/ajax/" ) {
        settings.url = "https://georemindme.appspot.com" + settings.url;
        //settings.xhrFields =  { withCredentials: true };
    }
});

Config = null;

$(document).ready(function() {
    
    var dialogSettings={
            autoOpen:false,
			resizable: false,
            buttons: [{
                    text: "Cerrar",
                    click: function() { $(this).dialog("close"); }
                }],
            draggable: false,
			width:560,
            
    }
    if(typeof($('#webapp'))=="undefined")
        dialogSettings['position'] = ['right', 45];
    else
        dialogSettings['position'] = ['top', 65];
        
    $('.help-txt').dialog(dialogSettings);
    
       
    //$('.help-icon img').click(function(){
    //    $('#'+$(this).attr('id')+'-text').dialog("open");
    //})
});

function facebookInit(config) {
    Config = config;

    FB.init(config);
    FB.Event.subscribe('auth.sessionChange', handleSessionChange);

    //FB.Canvas.setAutoResize();
    //if (typeof resizeIframe != "undefined") resizeIframe();
    // ensure we're always running on apps.facebook.com
    // if we are opening http://localhost:8080/fb/ or
    // georemindme.appspot.com/fb we will be redirected
    if (window == top && DEBUG_mode==false) { 
        alert(gettext("No puedes entrar a esta URL sin estar en Facebook, procedemos a redireccionarte"));
        goHome(); 
    }
}

function handleSessionChange(response) {
    //This checks if the user have changed the session and if it
    //is incoherent or there ir no session we move to home
    if ((Config.userIdOnServer && !response.session) ||
        Config.userIdOnServer != response.session.uid) 
    {
        //goHome();
    }
}

function goHome() {
    top.location = 'http://apps.facebook.com/' + Config.canvasName + '/';
}

function resizeIframe() {
    var tam=$('#right-col').height(); //Get height of the iframe
    //console.log("Entro y tam="+tam);
    //~ tam=tam+250;
    //~ console.log('Resize to '+tam);
    FB.Canvas.setSize({ height: tam });
    $('#right-col').css('min-height',tam+'px');
    
}

function grmLogged(){
    if($.cookies.get('georemindme_session_cookie')!="undefined")
        return true;
    else
        return false;
}


function check_ext_perm(session,callback) {
    
    var permArray=permissions.split(",");
    var query = FB.Data.query('select '+permissions+' from permissions where uid='+ session.userID);
    query.wait(function(rows) {
        var has_all_perms=true;
        permArray=permissions.split(",");
        for(perm in permArray){
            if(rows[0][permArray[perm]]!=1){
                has_all_perms=false
                break;
            }
        }
        if(has_all_perms) {
            callback(true);
        } else {
            callback(false);
        }
    });
};

function hasPerms(response){
    check_ext_perm(response.authResponse, function(isworking) {
        //Comprobamos si tenemos permisos para la app de FB
       if(isworking) {
          //window.location="/fb/dashboard/"
          return true
       } else {
          return false;
       }
    });
}
function haveLinkedAccount(uid){
    if(uid==null)
        return false;
    else
        return true;
}
function areCookiesCoherent(grm_cookie,fb_cookie){
    $.cookies.get('georemindme_session_cookie');
}

function loginApp(){
    FB.login(function(response) {
        tmp=response
        if (response.authResponse) {
            FB.api('/me', function(response) {
                //Redireccionamos
            });
        } else {
            //~ console.log('User cancelled login or did not fully authorize.');
        }
    }, {scope: permissions});
}

$(document).ready(function(){
    //if(typeof(resizeIframe)!="undefined")
        //if (typeof resizeIframe != "undefined") resizeIframe();
    setTimelineBehaviour();
            
        GRM.updateTabCounters();
        
        if($("#activity").length!=0){
            $('.load-more').attr("type","activity");
        }else if($("#public-profile").length!=0){
            $('.load-more').attr("type","timeline");
        }else if($("#notifications").length!=0){
            $('.load-more').attr("type","notifications");
        }
    

        
        //Adding behaviour to tab content
        $('#tabMenu li').not('.clear-box').click(function(){
            tab_id=$('#tabMenu li.active').attr('id')
            $('#'+tab_id+'_content').addClass('hidden');
            $('#tabMenu li.active').removeClass('active');
            
            tab_id=$(this).attr('id')
            $('#'+tab_id+'_content').removeClass('hidden');
            $(this).addClass('active');
        })
        
        $('#filter-suggestions').click(function(){
            $(':regex(class,(msg-300|msg-303))').show();
            //Oculto todos aquellos que no son sugerencias
            $('#chronology li').not('.msg-300').not('.msg-303').not('.suggestion-comment').hide();
        });
        
        $('#filter-lists').click(function(){
            $(':regex(class,(msg-350|msg-353))').show();
            //Oculto todos aquellos que no son sugerencias
            $('#chronology li').not('.msg-350').not('.msg-353').not('.suggestion-comment').hide();
        });
        
        $('#filter-likes').click(function(){
            $(':regex(class,(msg-125|msg-305|msg-355))').show();
            //Ocultamos aquellos que no son 125 ni 355
            $('#chronology li').not('.msg-125').not('.msg-305').not('.msg-355').hide()  
        });
            
        $('#filter-comments').click(function(){
            $(':regex(class,(msg-120|msg-121))').show();
            //Oculto todos aquellos que no son sugerencias
            $('#chronology li').not('.msg-120').not('.msg-121').hide();
        });
        
        $('#no-filter').click(function(){
            //Muestro todos
            $('#chronology li:not(.suggestion-comment)').show();
        });
        
        //$('.user-picture').each(function(i,elem){
            
        //    (new Image()).src = $(elem).attr('src')
        //})
        
        //Cargar más elementos del Timeline
        $(".load-more").loadTimeline({
                //'query_id':$(this).attr('value'),
                container:'#chronology'
            });
});

function setTimelineBehaviour(page){
    
    if (typeof page == "undefined" )
        page='';
    else
        page='li[value="'+page+'"] ';
    
    $(page + ".like-dislike").like();
    $(page + ".remember-forget").remember();
    $(page + ".removable").removable(); 
    showHideActionBar(page);
    setCommentsBehaviour(page);
    markUnreadItems(page);
}
function markUnreadItems(page){
    var notifications=$('#chronology').attr('notifications');
    if(notifications!='undefined'){
        var i=0;
        var msgs;
        if(page=='')
            msgs=$('#chronology > li');
        else
            msgs=$('#chronology > '+page);

        while (notifications > 0 && i < 10){
            $(msgs[i]).addClass("unread-item")
            notifications--;
            i++;
        }
        $('#chronology').attr('notifications',notifications)
    }
}

function showHideActionBar(page){
    //Show and hide action-bar
    $('#chronology '+ page +' div.timeline-msg,#chronology '+ page +' li.suggestion-comment').hover(
        function(){$(this).find('.action-bar').css('visibility','visible')},
        function(){$(this).find('.action-bar').css('visibility','hidden')}
    )
}

function setCommentsBehaviour(page){
    
    $(page+'.show-all-comments').click(function(){
        //Después de mostrar los comentarios ocultamos el botón
        $(this).parent().find('.long-list').slideDown('fast', function(){
            //if(typeof(resizeIframe)!="undefined")
                //if (typeof resizeIframe != "undefined") resizeIframe();
            $(this).parentsUntil('.suggestion-element').parent().find('.show-all-comments').remove();
            
        });
    });
    
    //Al pulsar en comentar ponemos el foco en el input
    $(page+'.focusInput').click(function(){
        var commentBox=$(this).parentsUntil('li').parent().find('.input-box')
        
        if(commentBox.hasClass('hidden'))
            commentBox.removeClass('hidden');
        
        commentBox.find('textarea').focus()
    });
    
    setCommentFormsBehaviour(page);
}

function setCommentFormsBehaviour(page){
    
    $(page+'.commentForm').find("textarea").focus(function(){
        $(this).css('color','black');
        if($(this).attr('empty')=="true"){
            var width=$(this).parent().parent().width()-45;
            $(this).css('width',width+'px');
            $(this).css('font-style','normal');
            $(this).css('font-size','1.1em');
            $(this).parent().parent().find("img").removeClass('hidden');
            //Guardamos y machamos el mensaje
            $(this).attr('msg',$(this).text())
            $(this).text("");
        }
    })
    
    $(page+'.commentForm').find("textarea").blur(function(){
        if($(this).val()=="")
            $(this).attr('empty',"true");
        
        if($(this).attr('empty')=="true")
            resetInput(this)
        
    })
    
    $(page+'.commentForm').find("textarea").keyup(function(e) {
        e.preventDefault();
        if(e.keyCode == 13) {
            //If keypress==enter -> submit
            element_id=$(this).parent().parent().parent().attr('value')
            parents=$(this).parentsUntil("#chronology")
            liElement=parents[parents.length-1]
            
            if($(liElement).hasClass('msg-350'))
                sendComment2($(this),element_id,"list");
            else
                sendComment2($(this),element_id,"event");
            
            $(this).val("");
            $(this).blur();
            resetInput(this)
            
            
        }else{
            var height=(parseInt($(this).val().length/55)+1)*1.2;
            if($(this).css('height')!=height)
                $(this).css('height',height+'em');
            if($(this).val().length>0)
                $(this).attr('empty',"false")
            else
                $(this).attr('empty',"true")
        }
    });
}

function resetInput(obj){
    var width=$(obj).parent().parent().width()-10;
    $(obj).css('width',width+'px');
    $(obj).css('color','#999');
    $(obj).css('font-style','italic');
    $(obj).css('font-size','0.9em');
    $(obj).parent().parent().find("img").addClass('hidden');
    
    //Reestablecemos el mensaje
    $(obj).attr('empty',"true")
    $(obj).text($(obj).attr('msg'));
    
    $(obj).focusout()
}

function sendComment2(textarea,element_id,elemType){
    if(textarea.val()=="")
        return false;
    else{
        msg=textarea.val();
        msg=msg.substring(0,msg.length-1);
    }
    GRM.wait();
    $.ajax({
        type: "POST",
        url: "/ajax/add/comment/"+elemType+"/",
        dataType:'json',
        data: {
            instance_id:element_id,
            msg:msg
        },
        complete: function() { GRM.nowait();},
        success: function(response){

            //console.log(response)
            textarea.parent()
            c=$('#commentTemplate').tmpl(response).appendTo('#commentList-'+element_id);
            c.find(".like-dislike").like();
            c.find(".removable").removable();
            //resetInput(textarea);
            //if(typeof(resizeIframe)!="undefined")
                //if (typeof resizeIframe != "undefined") resizeIframe();
        },
        error:{
        }
    });
}

function suggestionProposal(elem,action,timeline_id){
    
    //si se envia timeline_id por POST, se modificara ese timeline (se aceptara o rechazara la sugerencia)
    //status puede ser 0: nada 1: aceptada, 2: rechazada
    var data={};
    if(action=="accept")
        data['status']=1;
    else
        data['status']=2;
    data['timeline_id']=timeline_id;
    asd=elem;
    data["csrfmiddlewaretoken"]=$(elem).parent().find('input').val();
    
    GRM.wait();
    $.ajax({
        type: "POST",
        url: url["suggest_suggestion"],
        dataType:'json',
        data:data,
        context:$(this),
        complete: function() { GRM.nowait();},
        success: function(data){
            if(data==true){
                if(action=="accept")
                    $(elem).parent().empty().html(gettext("La propuesta ha sido aceptada"));
                else
                    $(elem).parent().empty().html(gettext("La propuesta ha sido rechazada"));
            }
            //~ $(elem).parent()
            //~ console.log(data);
        }
    })
}

