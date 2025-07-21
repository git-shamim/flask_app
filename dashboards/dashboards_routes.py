from flask import Blueprint, render_template

dashboards_bp = Blueprint("dashboards", __name__)

dashboards_data = {
    "un-comtrade": {
        "title": "🌐 UN COMTRADE: Global Trade Data",
        "description": "India's top trading partners, imports/exports by product.",
        "url": "https://lookerstudio.google.com/embed/reporting/your_un_comtrade_embed_url",
        "image": "images/dashboards/un_comtrade.jpg"
    },
    "world-bank-commodity-prices": {
        "title": "💰 World Bank Commodity Prices",
        "description": "Track price trends of energy, metals, and agricultural commodities.",
        "url": "https://lookerstudio.google.com/embed/reporting/your_world_bank_commodities_embed_url",
        "image": "images/dashboards/world_commodities.jpg"
    },
    "fao-trade": {
        "title": "🌾 FAO Trade: Agriculture Exports/Imports",
        "description": "India’s rice, wheat, pulses export/import dashboard.",
        "url": "https://lookerstudio.google.com/embed/reporting/your_fao_trade_embed_url",
        "image": "images/dashboards/fao_trade.jpg"
    },
    "world-development-indicators": {
        "title": "🌍 World Bank Development Indicators",
        "description": "Explore GDP, transport infrastructure, logistics index, and more.",
        "url": "https://lookerstudio.google.com/embed/reporting/your_world_dev_indicators_embed_url",
        "image": "images/dashboards/world_dev_indicators.jpg"
    }
}


@dashboards_bp.route("/dashboards")
def dashboard_list():
    return render_template("dashboards.html", dashboards=dashboards_data)

@dashboards_bp.route("/dashboards/<dashboard_name>")
def dashboard_view(dashboard_name):
    dashboard = dashboards_data.get(dashboard_name)
    if not dashboard:
        return render_template("404.html"), 404
    return render_template("dashboard_view.html", **dashboard)
