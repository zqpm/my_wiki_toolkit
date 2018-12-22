#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

pdf_options = {
    'page-size': 'A4',
    'margin-top': '12.7mm',
    'margin-bottom': '12.7mm',
    'margin-right': '12.7mm',
    'margin-left': '12.7mm',
    'disable-smart-shrinking': '',
    'dpi': '600',
    'zoom': '0.8',
    'title': '',
    'disable-internal-links': '',
    'footer-spacing': '2',
    'footer-font-name': 'serif',
    'footer-font-size': '10',
    'footer-center': 'I am trying to write something down to achieve the length for A4 footer XDDD                     [page] of [toPage]',
    'header-spacing': '2',
    'header-font-name': 'serif',
    'header-font-size': '10',
    'header-right': '[doctitle]',
    'disable-external-links': '',
    'print-media-type': '',
    'run-script': [
        'document.getElementById("footer").style.display = "none";',
        'document.getElementsByClassName("catlinks")[0].style.display = "none";',
        'document.getElementsByClassName("printfooter")[0].style.display = "none";',
        'document.getElementById("siteSub").style.display = "none";',
        'document.getElementById("CopyrightYear").innerText = "";',
    ]
}
