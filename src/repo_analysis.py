import logging

logger = logging.getLogger(__name__)

def analyze_repository(repo):
    try:
        repo_info = {
            "name": repo.name,
            "description": repo.description,
            "datasets": []
        }
        
        contents = repo.get_contents("datasets")
        for content_file in contents:
            if content_file.name.endswith('.csv'):
                repo_info["datasets"].append({
                    "name": content_file.name,
                    "path": content_file.path
                })
        
        return repo_info
    except Exception as e:
        logger.error(f"Error al analizar el repositorio: {e}")
        return None

