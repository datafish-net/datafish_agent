from flask import Blueprint, request, jsonify
from ..services.integration_service import IntegrationService

bp = Blueprint('integrations', __name__, url_prefix='/api/integrations')
integration_service = IntegrationService()

@bp.route('/execute', methods=['POST'])
def execute_integration():
    data = request.get_json()
    try:
        result = integration_service.execute(
            source_platform=data['sourcePlatform'],
            target_platform=data['targetPlatform'],
            source_data=data.get('data', {})
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400