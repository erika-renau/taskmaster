from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Project, Task

api_bp = Blueprint('api', __name__)

def current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

@api_bp.route('/projects', methods=['GET'])
@jwt_required()
def list_projects():
    user = current_user()
    projects = Project.query.filter_by(user_id=user.id).all()
    data = [{'id': p.id, 'title': p.title, 'description': p.description} for p in projects]
    return jsonify(data), 200

@api_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    user = current_user()
    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description', '')
    if not title:
        return jsonify({'msg':'title required'}), 400
    p = Project(title=title, description=description, user_id=user.id)
    db.session.add(p)
    db.session.commit()
    return jsonify({'id': p.id, 'title': p.title}), 201

@api_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@jwt_required()
def list_tasks(project_id):
    user = current_user()
    project = Project.query.filter_by(id=project_id, user_id=user.id).first_or_404()
    tasks = [{'id': t.id, 'title': t.title, 'done': t.done} for t in project.tasks]
    return jsonify(tasks), 200

@api_bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
@jwt_required()
def create_task(project_id):
    user = current_user()
    project = Project.query.filter_by(id=project_id, user_id=user.id).first_or_404()
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'msg':'title required'}), 400
    t = Task(title=title, description=data.get('description',''), project_id=project.id)
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id, 'title': t.title}), 201
