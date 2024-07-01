// vim: set et sw=2 ts=2 sts=2 ff=unix fenc=utf8:
// Author: Binux<i@binux.me>
//         http://binux.me
// Created on 2013-11-11 18:50:58

import EventEmitter from 'events'

function arrayEquals(a, b) {
    if (!a || !b)
        return false;
    if (a.length != b.length)
        return false;

    for (var i = 0, l = a.length; i < l; i++) {
        if (a[i] !== b[i])
            return false;
    }
    return true;
}

function getOffset(elem) {
    var top = 0;
    var left = 0;
    do {
        if ( !isNaN( elem.offsetLeft) ) left += elem.offsetLeft;
        if ( !isNaN( elem.offsetTop) ) top += elem.offsetTop;
    } while( elem = elem.offsetParent )
    return {top: top, left: left};
}

function merge_xpath(path, end) {
    var xpath = '';
    var prev = null;
    path.forEach(function(p, i) {
        if (end >= 0 && i > end) {
            return;
        }
        if (p.invalid) {
            prev = null;
        } else if (p.selected) {
            if (prev) {
                xpath += '/';
            }
            xpath += p.xpath;
            prev = p;
        } else {
            prev = null;
        }
    })
    if (xpath === '') {
        xpath = '//*';
    }
    return xpath;
}


function path_info(doc, element) {
    var path = [];
    do {
        var xpath = '';
        // get xpath
        var siblings = element.parentNode.childNodes;
        xpath = element.tagName.toLowerCase();
        for (var i=0, ix=0; siblings.length > 1 && i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element) {
                xpath += '['+(ix+1)+']';
                break;
            } else if (sibling.tagName == element.tagName) {
                ix++;
            }
        }

        // pack it up
        path.push({
            tag: element.tagName.toLowerCase(),
            xpath: xpath,
            selected: true,
            invalid: element.tagName.toLowerCase() === 'tbody',
        });
    } while (element = element.parentElement);

    path.reverse();

    // select elements
    var selected_elements = doc.querySelectorAll(merge_xpath(path));
    path.forEach(function(p, i) {
        if (p.invalid)
            return;
        p.selected = false;
        if (arrayEquals(selected_elements,
            doc.querySelectorAll(merge_xpath(path)))) {
            return;
        }
        p.selected = true;
    });

    return path;
}

export default class XPathSelectorHelperServer extends EventEmitter {
    constructor(window) {
        super();

        this.window = window;
        this.document = window.document;

        this.document.addEventListener("mouseover", (ev) => {
            this.overlay(ev.target);
        });

        this.document.addEventListener("click", (ev) => {
            ev.preventDefault();
            ev.stopPropagation();

            this.emit('selector_helper_click', path_info(this.document, ev.target));
        });
    }

    overlay(elements) {
        if (typeof elements === 'string') {
            elements = this.document.querySelectorAll(elements);
        }
        if (elements instanceof this.window.Element) {
            elements = [elements];
        }
        [...this.document.querySelectorAll('.pyspider_overlay')].forEach((elem) => {
            elem.remove();
        });
        [...elements].forEach((elem) => {
            const offset = getOffset(elem);
            const div = this.document.createElement("div");
            div.className = "pyspider_overlay";
            div.setAttribute('style', 'z-index: 999999;background-color: rgba(255, 165, 0, 0.3);position: absolute;pointer-events: none;'
                +'top: '+offset.top+'px;'
                +'left:'+offset.left+'px;'
                +'width: '+elem.offsetWidth+'px;'
                +'height: '+elem.offsetHeight+'px;');
            this.document.body.appendChild(div);
        });
    }

    heightlight(elements) {
        if (typeof elements === 'string') {
            elements = this.document.querySelectorAll(elements);
        }
        console.log(elements);
        if (elements instanceof this.window.Element) {
            elements = [elements];
        }
        [...this.document.querySelectorAll('.pyspider_highlight')].forEach((elem) => {
            elem.remove();
        });
        [...elements].forEach((elem) => {
            const offset = getOffset(elem);
            const div = this.document.createElement("div");
            div.className = "pyspider_highlight";
            div.setAttribute('style', 'z-index: 888888;border: 2px solid #c00;position: absolute;pointer-events: none;'
                +'top: '+(offset.top-2)+'px;'
                +'left:'+(offset.left-2)+'px;'
                +'width: '+elem.offsetWidth+'px;'
                +'height: '+elem.offsetHeight+'px;');
            this.document.body.appendChild(div);
        });
    }

    getElementByXpath(path) {
        return this.document.evaluate(path, this.document, null, this.window.XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }
}