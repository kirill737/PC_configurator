from flask import (
    request, 
    jsonify,
)

from controllers.db.component_controller import (
    change_component,
    delete_component,
)
from logger_settings import setup_logger


logger = setup_logger("options_menu")


def init_edit_component_menu(app):

    @app.route("/change/component", methods=["POST"])
    def change_component_view():
        logger.info("Попытка изменить данные...")
        
        data = request.json
        if change_component(data.get("id"), data.get("price"), data.get("info")):
            return jsonify({"status": "success"})

        return jsonify({"status": "error", "message": "Failed to edit component"})

    
    @app.route("/delete/component/<int:component_id>")
    def delete_component_view(component_id):
        logger.info("Попытка удалить деталь..."
                    )
        result = delete_component(component_id)
        if result is None:
            return jsonify({"status": "success"})
        
        return jsonify({"status": "error", "message": result})