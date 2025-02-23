from flask import Blueprint, request, jsonify
from ..services.knowledge_service import KnowledgeService

bp = Blueprint('knowledge', __name__, url_prefix='/api/knowledge')
knowledge_service = KnowledgeService()

@bp.route('/platform', methods=['POST'])
def add_platform_knowledge():
    data = request.get_json()
    platform = data.get('platform')
    documentation = data.get('documentation')
    
    try:
        knowledge_service.add_platform_knowledge(platform, documentation)
        return jsonify({'message': 'Knowledge base updated'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/mapping', methods=['POST'])
def add_mapping_knowledge():
    data = request.get_json()
    source_platform = data.get('sourcePlatform')
    target_platform = data.get('targetPlatform')
    mappings = data.get('mappings')
    
    try:
        knowledge_service.add_mapping_knowledge(source_platform, target_platform, mappings)
        return jsonify({'message': 'Mapping knowledge added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400