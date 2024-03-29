from icon_lister import *
import time

ignore_list = [
    "us_air_c47_para",
    "civilianCar2",
    "arg_jet_a1h_objective",
    "ru_ahe_ka29t",
    "ru_ahe_mi8amtsh",
    "ch_ahe_z9wa"
]

def makeHead(title):
    return [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<title>{}</title>".format(title),
        "<style>",
        "html {"
        "    font: 1rem/1.5 Arial, sans-serif;",
        "    background: lightgray;",
        "}",
        "div.outer {",
        "    text-align: center;",
        "    margin-left: auto;",
        "    margin-right: auto;",
        "}",
        "div.inner {",
        "    display: inline-block;",
        "}",
        "img {",
        "    image-rendering: -moz-crisp-edges;",
        "    image-rendering: -webkit-optimize-contrast;",
        "    image-rendering: crisp-edges;",
        "    -ms-interpolation-mode: nearest-neighbor;",
        "    height: 64px;",
        "    text-align: center;",
        "}",
        "table {",
        "    display: table;",
        "    width: 100%;",
        "    text-align: left;",
        "}",
        "td {",
        "    border: 1px solid black;",
        "    vertical-align: top;",
        "    padding: 8px;",
        "}",
        "span {",
        "    display: block;",
        "}",
        "</style>",
        "</head>",
        "<body>",
        "",
        "<div class=\"outer\">",
        "<div class=\"inner\">",
        "",
        "<h1>{}</h1>".format(title),
        "",
    ]

tail = [
    "",
    "</div>",
    "</div>",
    "",
    "</body>",
    "</html>",
]

facTr = {
    "civ": "Civilian",
    "gb82": "GB",
    "mil": "Militia",
    "boat": "Generic"
}

def vehToFactionName(veh):
    vehOrig = veh
    fac = None
    
    for i in range(2, 5):
        if veh[i] == "_":
            fac = veh[:i]
            break
    
    if veh in names_map:
        veh = names_map[veh]
        if veh[0] == "\"":
            veh = veh[1:]
        if veh[-1] == "\"":
            veh = veh[:-1]
    else:
        print("No HUD name found for: {}".format(vehOrig))
    
    if fac == None:
        print("Unknown faction: {}".format(vehOrig))
        return veh
    
    if fac in facTr:
        fac = facTr[fac]
    else:
        fac = fac.upper()
    
    return (fac, veh)

if __name__ == "__main__":
    # ########################################################################################
    # index.html
    # ########################################################################################
    file = os.path.join(os.path.curdir + "/index.html")
    print(file)

    lines = []
    lines.extend(makeHead("PR Assets Indexes"))
    lines.extend([
        "<h2>Automatically generated at {} using a script by CAS_ual_TY</h2>".format(time.asctime()),
        "<h2>Vehicles</h2>",
        "<span><a href=\"icon-to-asset_index.html\">PR Icon-to-Assets Index (click here)</a></span>",
        "<span><a href=\"asset-to-icon_index.html\">PR Assets-to-Icon Index (click here)</a></span>"
        "<span><a href=\"faction-asset-to-icon_index.html\">PR Faction-Assets-to-Icon Index (click here)</a></span>",
        "<h2>Kits</h2>",
        "<span><a href=\"icon-to-kit_index.html\">PR Icon-to-Kit Index (click here)</a></span>",
    ])
    lines.extend(tail)

    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()

    # ########################################################################################
    # Icon -> Asset Index
    # ########################################################################################

    file = os.path.join(os.path.curdir + "/icon-to-asset_index.html")
    print(file)

    lines = []
    lines.extend(makeHead("PR Icon-to-Assets Index"))
    lines.append("<a href=\"index.html\">Return to Index</a>")
    lines.extend([
        "<h3>Sorted alphabetically by asset name (ignoring faction identifier in front).</h3>",
        "<table>",
        "<hr>",
    ])
    
    for k, v in icons_map.items():
        v = [a for a in v if a not in ignore_list]
        if k[:len("mini_")] == "mini_" and len(v) > 0:
            i = k[len("mini_"):-len(".tga")]
            lines.append("<tr>")
            lines.append("<td><img src=\"./vehicles/{}\"></td>".format("mini_" + i + ".png"))
            lines.append("<td>")
            lines.append("<b>{}</b>:".format(i))
            lines.append("<ul>")
            for v2 in v:
                if v2[-len(bf2):] != bf2 and v2[-len(prsp):] != prsp and v2[-len(sp):] != sp:
                    fac, veh = vehToFactionName(v2)
                    lines.append("<li>{} <b>{}</b> ({})</li>".format(fac, veh, v2))
            lines.append("</ul>")
            lines.append("</td>")
            lines.append("</tr>")
    
    lines.extend([
        "",
        "</table>"
    ])
    
    lines.extend(tail)
    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()

    # ########################################################################################
    # Asset -> Icon Index
    # ########################################################################################

    file = os.path.join(os.path.curdir + "/asset-to-icon_index.html")
    print(file)
    
    lines = []
    lines.extend(makeHead("PR Assets-to-Icon Index"))
    lines.append("<a href=\"index.html\">Return to Index</a>")
    lines.extend([
        "<h3>Sorted alphabetically by asset name (ignoring faction identifier in front).</h3>",
        "<hr>",
        "<table>"
    ])
    
    assets = []
    
    for k, v in icons_map.items():
        v = [a for a in v if a not in ignore_list]
        if k[:len("mini_")] == "mini_" and len(v) > 0:
            for v2 in v:
                if v2[-len(bf2):] != bf2 and v2[-len(prsp):] != prsp and v2[-len(sp):] != sp:
                    assets.append(vehToFactionName(v2) + (v2, k[len("mini_"):-len(".tga")],))
    
    sortedAssets = sorted(assets, key=lambda tup: tup[1])

    for fac, name, veh, icon in sortedAssets:
        lines.append("<tr>")
        lines.append("<td><img src=\"./vehicles/{}\"></td>".format("mini_" + icon + ".png"))
        lines.append("<td>{} <b>{}</b> ({}, {})</td>".format(fac, name, veh, icon))
        lines.append("</tr>")
    
    lines.extend([
        "",
        "</table>"
    ])
    lines.extend(tail)
    
    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()

    # ########################################################################################
    # Faction, Asset -> Icon Index
    # ########################################################################################

    file = os.path.join(os.path.curdir + "/faction-asset-to-icon_index.html")
    print(file)
    
    lines = []
    lines.extend(makeHead("PR Faction-Assets-to-Icon Index"))
    lines.append("<a href=\"index.html\">Return to Index</a>")
    lines.extend([
        "<h3>Sorted alphabetically by factions and asset name.</h3>"
    ])
    
    sortedAssets = sorted(assets, key=lambda tup: (tup[0], tup[1]))

    fac0 = None

    for fac, name, veh, icon in sortedAssets:
        if fac0 != fac:
            if fac0 != None:
                lines.append("</table>")
            fac0 = fac
            lines.append("<hr>")
            lines.append("<h2>{}</h2>".format(fac))
            lines.append("<table>")
        lines.append("<tr>")
        lines.append("<td><img src=\"./vehicles/{}\"></td>".format("mini_" + icon + ".png"))
        lines.append("<td>{} <b>{}</b> ({}, {})</td>".format(fac, name, veh, icon))
        lines.append("</tr>")
    
    lines.append("</table>")
    lines.extend(tail)
    
    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()

    # ########################################################################################
    # Icon -> Kit Index
    # ########################################################################################

    file = os.path.join(os.path.curdir + "/icon-to-kit_index.html")
    print(file)
    
    lines = []
    lines.extend(makeHead("PR Icon-to-Kit Index"))
    lines.append("<a href=\"index.html\">Return to Index</a>")
    lines.extend([
        "<h3>Sorted alphabetically by kit identifier.</h3>"
        "<hr>",
        "<table>"
    ])
    
    for f in os.listdir(os.path.join(os.path.curdir + "/kits")):
        if f[-len("_outline.png"):] == "_outline.png":
            lines.append("<tr>")
            lines.append("<td><img src=\"./kits/{}\"></td>".format(f))
            lines.append("<td>{}</td>".format(f[:-len("_outline.png")]))
            lines.append("</tr>")
    
    lines.append("</table>")
    lines.extend(tail)
    
    with open(file, "w") as f:
        f.writelines([l + "\n" for l in lines])
        f.close()
