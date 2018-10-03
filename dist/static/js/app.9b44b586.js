(function(e){function t(t){for(var n,i,o=t[0],c=t[1],d=t[2],u=0,h=[];u<o.length;u++)i=o[u],r[i]&&h.push(r[i][0]),r[i]=0;for(n in c)Object.prototype.hasOwnProperty.call(c,n)&&(e[n]=c[n]);l&&l(t);while(h.length)h.shift()();return s.push.apply(s,d||[]),a()}function a(){for(var e,t=0;t<s.length;t++){for(var a=s[t],n=!0,o=1;o<a.length;o++){var c=a[o];0!==r[c]&&(n=!1)}n&&(s.splice(t--,1),e=i(i.s=a[0]))}return e}var n={},r={app:0},s=[];function i(t){if(n[t])return n[t].exports;var a=n[t]={i:t,l:!1,exports:{}};return e[t].call(a.exports,a,a.exports,i),a.l=!0,a.exports}i.m=e,i.c=n,i.d=function(e,t,a){i.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},i.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.t=function(e,t){if(1&t&&(e=i(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(i.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)i.d(a,n,function(t){return e[t]}.bind(null,n));return a},i.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return i.d(t,"a",t),t},i.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},i.p="/";var o=window["webpackJsonp"]=window["webpackJsonp"]||[],c=o.push.bind(o);o.push=t,o=o.slice();for(var d=0;d<o.length;d++)t(o[d]);var l=c;s.push([0,"chunk-vendors"]),a()})({0:function(e,t,a){e.exports=a("56d7")},"11fe":function(e,t,a){"use strict";var n=a("9147"),r=a.n(n);r.a},2856:function(e,t,a){},"56d7":function(e,t,a){"use strict";a.r(t);a("cadf"),a("551c"),a("097d");var n=a("2b0e"),r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"clearfix"},[e._m(0),a("router-view")],1)},s=[function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("header",[a("nav",{staticClass:"navbar navbar-expand-md navbar-dark bg-dark fixed-top"},[a("a",{staticClass:"navbar-brand",attrs:{href:"#"}},[e._v("Manual Evaluation")])])])}],i=(a("5c0b"),a("2877")),o={},c=Object(i["a"])(o,r,s,!1,null,null,null);c.options.__file="App.vue";var d=c.exports,l=a("8c4f"),u=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("main",{staticClass:"container-fluid, home",attrs:{role:"main"}},[a("Editor")],1)},h=[],m=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card col-8"},[a("div",{staticClass:"card-header"},[e._v("Document")]),a("div",{staticClass:"card-body document",domProps:{innerHTML:e._s(e.message)},on:{mouseup:e.captureHighlight}})]),e._m(0)]),a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card col-11 lower-card"},[a("div",{staticClass:"card-header"},[e._v("Summary")]),a("div",{staticClass:"card-body col highlights",domProps:{innerHTML:e._s(e.markedText)}})]),a("div",{staticClass:"card col-1 lower-card"},[a("div",{staticClass:"card-header"},[e._v("Words Left")]),a("div",{staticClass:"card-body"},[e._v(e._s(e.wordsLeft))])])]),a("div",{staticClass:"row float-right"},[a("router-link",{attrs:{to:{name:"surveyForm",params:{markedTextIdxs:this.markedTextIdxs}},tag:"button"}},[e._v("\n      Submit\n    ")])],1)])},v=[function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"card col-4"},[a("div",{staticClass:"card-header"},[e._v("Guidelines")]),a("div",{staticClass:"card-body"},[a("p",[e._v("You have been given a document and guidelines to help you form a summary. Please read the document and then highlights fragments of sentences to form a 100 words summary based on the following guidelines.")]),a("p",[e._v("1. The summary tells you who was involved in the document narration and\n        the information is correct.")]),a("p",[e._v("2. The summary tells you what had happened in the document narration and\n        the information is correct.")]),a("p",[e._v("3. The summary tells you where the event took place in the document\n        narration and the information is correct.")]),a("p",[e._v("4. The summary tells you when did the event happen in the document\n        narration and the information is correct.")]),a("p",[e._v("5. The summary tells you why did the event happen in the document\n        narration and the information is correct.")]),a("p",[e._v("6. The summary tells you how did the event happen in the document\n        narration and the information is correct.")])])])}],f=(a("6b54"),a("28a5"),a("fd9b")),p="",g=0;function _(e){var t=new XMLHttpRequest;t.open("get",e,!1),t.onreadystatechange=function(){4===t.readyState&&(200!==t.status&&0!==t.status||(p=t.responseText))},t.send(null)}function y(e){for(var t=e.trim().split(" "),a=0,n=0;n<t.length;n+=1)""!==t[n]&&(a+=1);return a}var b={methods:{captureHighlight:function(e){var t="",a=[];if(null!=sessionStorage.getItem("selections")&&(a=JSON.parse(sessionStorage.getItem("selections"))),window.getSelection?t=window.getSelection():document.getSelection?t=document.getSelection():document.selection&&(t=document.selection.createRange().text),this.wordCount+y(t.toString())<=100){var n=f({luminosity:"light"});a.push([t.anchorOffset,t.focusOffset]),this.index=a,this.markedText="".concat(this.markedText," <div style='background-color: ").concat(n,";'><span class='highlightID' >[").concat(g,"]</span> ").concat(t.toString(),"</div>"),sessionStorage.setItem("selections",JSON.stringify(a));var r=t.getRangeAt(0),s=document.createNodeIterator(r.commonAncestorContainer,NodeFilter.SHOW_ALL,{acceptNode:function(e){return NodeFilter.FILTER_ACCEPT}}),i=[];while(s.nextNode())if(0!==i.length||s.referenceNode===r.startContainer){if(i.push(s.referenceNode),"SPAN"===s.referenceNode.parentElement.nodeName){var o=s.referenceNode.parentElement.parentElement,c=s.referenceNode.parentElement;this.markedTextIdxs.push(Array.prototype.indexOf.call(o.children,c)),s.referenceNode.parentElement.setAttribute("style","background-color: ".concat(n,";"))}if(s.referenceNode===r.endContainer)break}}else alert("Max words are 100");g+=1,window.getSelection?window.getSelection().empty?window.getSelection().empty():window.getSelection().removeAllRanges&&window.getSelection().removeAllRanges():document.selection&&document.selection.empty()}},data:function(){_("/static/gold_doc/PROXY_LTW_ENG_20070831_0072");for(var e="",t=0;t<p.length;t+=1)e+="<span>".concat(p[t],"</span>");return this.message=e,{message:this.message,index:[],markedText:"",markedTextIdxs:[],isActive:!1}},computed:{wordsLeft:function(){return 100-this.wordCount},wordCount:function(){return this.markedText?y(this.markedText):0},charIndex:function(){return this.markedTextIdxs?this.markedTextIdxs:""}}},x=b,C=(a("7a73"),Object(i["a"])(x,m,v,!1,null,"bbf25242",null));C.options.__file="HighlightEditor.vue";var k=C.exports,w={components:{Editor:k}},T=w,S=(a("6521"),Object(i["a"])(T,u,h,!1,null,null,null));S.options.__file="Annotation.vue";var E=S.exports,I=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("main",{staticClass:"container-fluid, home",attrs:{role:"main"}},[a("Survey")],1)},O=[],$=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card col-8"},[a("div",{staticClass:"card-header"},[e._v("Document")]),a("div",{staticClass:"card-body document",domProps:{innerHTML:e._s(e.message)}})]),e._m(0)]),a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card"},[a("div",{staticClass:"card-header"},[e._v("\n              Filter\n            ")]),a("div",{staticClass:"card-body"},[e._m(1),a("div",{staticClass:"row"},[a("div",{staticClass:"my-checkbox col-2"},[a("input",{directives:[{name:"model",rawName:"v-model",value:e.checked,expression:"checked"}],attrs:{type:"checkbox"},domProps:{checked:Array.isArray(e.checked)?e._i(e.checked,null)>-1:e.checked},on:{change:function(t){var a=e.checked,n=t.target,r=!!n.checked;if(Array.isArray(a)){var s=null,i=e._i(a,s);n.checked?i<0&&(e.checked=a.concat([s])):i>-1&&(e.checked=a.slice(0,i).concat(a.slice(i+1)))}else e.checked=r}}}),e._v("Enable Heatmap\n                ")]),a("div",{staticClass:"col-10"},[a("VueSlideBar",{attrs:{data:e.slider.data,range:e.slider.range,labelStyles:{color:"#4a4a4a",backgroundColor:"#4a4a4a"},processStyle:{backgroundColor:"#d8d8d8"}},on:{callbackRange:e.callbackRange},model:{value:e.value,callback:function(t){e.value=t},expression:"value"}})],1)])])])]),e._m(2),e._m(3),e._m(4),e._m(5),e._m(6),e._m(7)])},A=[function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"card col-4"},[a("div",{staticClass:"card-header"},[e._v("Guidelines")]),a("div",{staticClass:"card-body"},[a("p",[e._v("You have been given a document where some of its words are highlighted.\n              These highlighted words depict important words to the document.\n              Please read the document and then rate the given summaries\n              based on the following guidelines.")]),a("p",[e._v("1. The summary tells you who was involved in the document narration and\n            the information is correct.")]),a("p",[e._v("2. The summary tells you what had happened in the document narration and\n            the information is correct.")]),a("p",[e._v("3. The summary tells you where the event took place in the document\n            narration and the information is correct.")]),a("p",[e._v("4. The summary tells you when did the event happen in the document\n            narration and the information is correct.")]),a("p",[e._v("5. The summary tells you why did the event happen in the document\n            narration and the information is correct.")]),a("p",[e._v("6. The summary tells you how did the event happen in the document\n            narration and the information is correct.")])])])},function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"row"},[a("div",{staticClass:"col"},[a("p",[e._v("\n                Words in the document that are deemed important have been highlighted by participants and presented using heat map visualization.\n                The deeper the color, the more participants who have higlighted it.\n                You can disable the heatmap and instead filtering the color using the slider to restrict by the number of person who have higlighted the words.\n                ")])])])},function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card"},[a("div",{staticClass:"card-header"},[e._v("Summary 1")]),a("div",{staticClass:"card-body col"},[e._v("u.s and european officials may impose a 4th round of sanctions on tehran when the u.n , security council considers the issue of iran 's nuclear energy program most likely in september 2007 . ")])])])},function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card"},[a("div",{staticClass:"card-header"},[e._v("Evaluation 1")]),a("div",{staticClass:"card-body col"},[a("p",[e._v("The given summary is informative in term of the six criteria (see the guidance).")]),a("label",{staticClass:"float-left",attrs:{for:""}},[e._v("Disagree")]),a("label",{staticClass:"float-right",attrs:{for:""}},[e._v("Agree")]),a("input",{staticClass:"slider",attrs:{type:"range",min:"1",max:"100",value:"50"}})])])])},function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card"},[a("div",{staticClass:"card-header"},[e._v("Summary 2")]),a("div",{staticClass:"card-body col"},[e._v("The International Atomic Energy Agency distributed limited copies of the European nuclear energy program masks an effort to obtain technology that could be used in the production of nuclear bomb material that could be used in the production of the uranium and the U.S. sanctions on Tehran when the U.N. Security Council considers the issue .")])])])},function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card"},[a("div",{staticClass:"card-header"},[e._v("Evaluation 2")]),a("div",{staticClass:"card-body col"},[a("p",[e._v("The given summary is informative in term of the six criteria (see the guidance).")]),a("label",{staticClass:"float-left",attrs:{for:""}},[e._v("Disagree")]),a("label",{staticClass:"float-right",attrs:{for:""}},[e._v("Agree")]),a("input",{staticClass:"slider",attrs:{type:"range",min:"1",max:"100",value:"50"}})])])])},function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card"},[a("div",{staticClass:"card-header"},[e._v("Summary 3")]),a("div",{staticClass:"card-body col"},[e._v("A masked nuclear energy program is suspected of the international civilian energy energy program in Europe and Iran 's efforts to obtain technology used to produce the atomic bombs used to produce the atomic bomb when the U.N. Security Council considers it .")])])])},function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"row card-deck"},[a("div",{staticClass:"card"},[a("div",{staticClass:"card-header"},[e._v("Evaluation 3")]),a("div",{staticClass:"card-body col"},[a("p",[e._v("The given summary is informative in term of the six criteria (see the guidance).")]),a("label",{staticClass:"float-left",attrs:{for:""}},[e._v("Disagree")]),a("label",{staticClass:"float-right",attrs:{for:""}},[e._v("Agree")]),a("input",{staticClass:"slider",attrs:{type:"range",min:"1",max:"100",value:"50"}})])])])}],N=(a("ac6a"),a("4f7f"),a("8afe")),P=(a("55dd"),a("add7")),j=a.n(P),L=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,2101,2102,2103,2104,2105,2106,2107,2108,2109,2110,2111,2112,2113,2114,2115,2116,2117,2118,2119,2120,2121,2122,2123,2124,2125,2126,2127,2128,2129,2130,2131,2132,2133,2134,2135,2136,2137,2138,2139,2140,2141,2142,2143,2144,2145,2146,2147,2148,2149,2150,2151,2152,2153,2154,2155,2156,2157,2158,2159,2160,2161,2162,2163,2164,2165,2166,2167,2168,2169,2170,2171,2172,2173,2174,2175,2176,2177,2178,2179,2180,2181,2182,2183,2184,2185,2186,2187,2188,2189,2190,2191,2192,2193,2194,2195,2196,2197,2198,2199,2200,2201,2202,2203,2204,2205,2206,2207,2208,2209,2210,2211,2212,2213,2214,2215,2216,2217,2218,2219,2220,2221,2222,2223,2224,2225,2226,2227,2228,2229,2230,2231,2232,2233,2234,2235,2236,2237,2238,2239,2240,2241,2242,2243,2244,2245,2246,2247,2248,2249,2250,2251,2252,2253,2254,2255,2256,2257,2258,2259,2260,2261,2262,2263,2264,2265,2266,2267,2268,2269,2270,2271,2272,2273,2274,2275,2276,2277,2278,2279,2280,2281,2282,2283,2284,2285,2286,2287,2288,2289,2290,2291,2292,2293,2294,2295,2296,2297,2298,2299,2300,2301,2302,2303,2304,2305,2306,2307,2308,2309,2310,2311,2312,2313,2314,2315,2316,3705,3706,3707,3708,3709,3710,3711,3712,3713,3714,3715,3716,3717,3718,3719,3720,3721,3722,3723,3724,3725,3726,3727,3728,3729,3730,3731,3732,3733,3734,3735,3736,3737,3738,3739,3740,3741,3742,3743,3744,3745,3746,3747,3748,3749,3750,3751,3752,3753,3754,3755,3756,3757,3758,3759,3760,3761,3762,3763,3764,3765,3766,3767,3768,3769,3770,3771,3772,3773,3774,3775,3776,3777,3778,3779,3780,3781,3782,3783,3784,3785,3786,3787,3788,3789,3790,3791,3792,3793,3794,3795,3796,3797,3798],R=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,1833,1834,1835,1836,1837,1838,1839,1840,1841,1842,1843,1844,1845,1846,1847,1848,1849,1850,1851,1852,1853,1854,1855,1856,1857,1858,1859,1860,1861,1862,1863,1864,1865,1866,1867,1868,1869,1870,1871,1872,1873,1874,1875,1876,1877,1878,1879,1880,1881,1882,1883,1884,1885,1886,1887,1888,1889,1890,1891,1892,1893,1894,1895,1896,1897,1898,1899,1900,1901,1902,1903,1904,1905,1906,1907,1908,1909,1910,1911,1912,1913,1914,1915,1916,1917,1918,1919,1920,1921,1922,1923,1924,1925,1926,1927,1928,1929,1930,1931,1932,1933,1934,1935,1936,1937,1938,1939,1940,1941,1942,1943,1944,1945,1946,1947,1948,1949,1950,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2e3,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036,2037,2038,2039,2040,2041,2042,2043,2044,2045,2046,2047,2048,2049,2050,2051,2052,2053,2054,2055,2056,2057,2058,2059,2060,2061,2062,2063,2064,2065,2066,2067,2068,2069,2070,2071,2072,2073,2074,2075,2076,2077,2078,2079,2080,2081,2082,2083,2084,2085,2086,2087,2088,2089,2090,2091,2092,2093,2094,2095,2096,2097,2098,2099,2100,3594,3595,3596,3597,3598,3599,3600,3601,3602,3603,3604,3605,3606,3607,3608,3609,3610,3611,3612,3613,3614,3615,3616,3617,3618,3619,3620,3621,3622,3623,3624,3625,3626,3627,3628,3629,3630,3631,3632,3633,3634,3635,3636,3637,3638,3639,3640,3641,3642,3643,3644,3645,3646,3647,3648,3649,3650,3651,3652,3653,3654,3655,3656,3657,3658,3659,3660,3661,3662,3663,3664,3665,3666,3667,3668,3669,3670,3671,3672,3673,3674,3675,3676,3677,3678,3679,3680,3681,3682,3683,3684,3685,3686,3687,3688,3689,3690,3691,3692,3693,3694,3695,3696,3697,3698,3699,3700,3701,3702,3703,3704],M=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,3704,3705,3706,3707,3708,3709,3710,3711,3712,3713,3714,3715,3716,3717,3718,3719,3720,3721,3722,3723,3724,3725,3726,3727,3728,3729,3730,3731,3732,3733,3734,3735,3736,3737,3738,3739,3740,3741,3742,3743,3744,3745,3746,3747,3748,3749,3750,3751,3752,3753,3754,3755,3756,3757,3758,3759,3760,3761,3762,3763,3764,3765,3766,3767,3768,3769,3770,3771,3772,3773,3774,3775,3776,3777,3778,3779,3780,3781,3782,3783,3784,3785,3786,3787,3788,3789,3790,3791,3792,3793,3794,3795,3796,3797,3798,3799,3800,3801,3802,3803,3804,3805,3806,3807,3808,3809,3810,3811,3812,3813,3814,3815,3816,3817,3818,3819,3820,3821,3822,3823,3824,3825,3826,3827,3828,3829,3830,3831,3832,3833,3834,3835,3836,3837,3838,3839,3840,3841,3842,3843,3844,3845,3846,3847,3848,3849,3850,3851,3852,3853,3854,3855,3856,3857,3858,3859,3860,3861,3862,3863,3864,3865,3866,3867,3868],H="";function F(e){var t,a=[],n=[];e.sort();for(var r=0;r<e.length;r+=1)e[r]!==t?(a.push(e[r]),n.push(1)):n[n.length-1]+=1,t=e[r];for(var s=-1,i=0;i<n.length;i+=1)n[i]>s&&(s=n[i]);for(var o=Object(N["a"])(new Set(n)),c=n.slice(),d=0;d<n.length;d+=1)c[d]=n[d]/s;return[a,c,o,n]}function D(e){var t=new XMLHttpRequest;t.open("get",e,!1),t.onreadystatechange=function(){4===t.readyState&&(200!==t.status&&0!==t.status||(H=t.responseText))},t.send(null)}var W={methods:{callbackRange:function(e){this.rangeValue=e}},computed:{charIndex:function(){return this.$route.params.markedTextIdxs?this.$route.params.markedTextIdxs:"empty"}},components:{VueSlideBar:j.a},watch:{checked:function(e){var t;this.$route.params.markedTextIdxs&&(this.markedTextIdxs=this.$route.params.markedTextIdxs.concat(L).concat(R).concat(M),t=F(this.markedTextIdxs));for(var a="",n=0;n<H.length;n+=1){var r=t[0].indexOf(n),s=void 0;-1===r?a+="<span>".concat(H[n],"</span>"):this.checked?(s=t[1][r],a+='<span style="background-color: rgba(255, 110, 0, '.concat(s,')"}>').concat(H[n],"</span>")):(s=t[3][r],s===this.value?a+='<span style="background-color: rgba(255, 110, 0)"}>'.concat(H[n],"</span>"):a+="<span>".concat(H[n],"</span>"))}this.message=a},value:function(e){var t;this.$route.params.markedTextIdxs&&(this.markedTextIdxs=this.$route.params.markedTextIdxs.concat(L).concat(R).concat(M),t=F(this.markedTextIdxs));for(var a="",n=0;n<H.length;n+=1){var r=t[0].indexOf(n),s=void 0;-1===r?a+="<span>".concat(H[n],"</span>"):this.checked?(s=t[1][r],a+='<span style="background-color: rgba(255, 110, 0, '.concat(s,')"}>').concat(H[n],"</span>")):(s=t[3][r],a+=s===e?'<span style="background-color: rgba(255, 110, 0)"}>'.concat(H[n],"</span>"):"<span>".concat(H[n],"</span>"))}this.message=a}},data:function(){var e;D("static/gold_doc/PROXY_LTW_ENG_20070831_0072"),this.$route.params.markedTextIdxs&&(this.markedTextIdxs=this.$route.params.markedTextIdxs.concat(L).concat(R).concat(M),e=F(this.markedTextIdxs));for(var t="",a=0;a<H.length;a+=1){var n=e[0].indexOf(a),r=void 0;-1===n?t+="<span>".concat(H[a],"</span>"):(r=e[1][n],t+='<span style="background-color: rgba(255, 110, 0, '.concat(r,')"}>').concat(H[a],"</span>"))}for(var s=[],i=0;i<e[2].length;i+=1)s.push({label:e[2][i]});return{message:t,markedTextIdxs:[],value:1,slider:{data:e[2].reverse(),range:s.reverse()},checked:!0}}},Y=W,G=(a("11fe"),Object(i["a"])(Y,$,A,!1,null,"96e10894",null));G.options.__file="Survey.vue";var J=G.exports,X={components:{Survey:J}},U=X,V=(a("6b91"),Object(i["a"])(U,I,O,!1,null,null,null));V.options.__file="SurveyForm.vue";var q=V.exports;n["a"].use(l["a"]);var B=new l["a"]({routes:[{path:"/",name:"annotation",component:E},{path:"/survey",name:"surveyForm",component:q}]});n["a"].config.productionTip=!1,new n["a"]({router:B,render:function(e){return e(d)}}).$mount("#app")},"5c0b":function(e,t,a){"use strict";var n=a("2856"),r=a.n(n);r.a},6521:function(e,t,a){"use strict";var n=a("881e"),r=a.n(n);r.a},"6b91":function(e,t,a){"use strict";var n=a("aff5"),r=a.n(n);r.a},"7a73":function(e,t,a){"use strict";var n=a("a36e"),r=a.n(n);r.a},"881e":function(e,t,a){},9147:function(e,t,a){},a36e:function(e,t,a){},aff5:function(e,t,a){}});
//# sourceMappingURL=app.9b44b586.js.map