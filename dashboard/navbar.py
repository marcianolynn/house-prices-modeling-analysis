import dash_bootstrap_components as dbc


def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("The Variables", href="/variables")),
            dbc.NavItem(dbc.NavLink("Exploratory Data Analysis", href="/eda")),
            dbc.NavItem(dbc.NavLink("Models", href="/models"))
        ],
        brand="Home",
        brand_href="/home",
        sticky="top",
    )
    return navbar
