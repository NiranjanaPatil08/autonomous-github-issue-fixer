import os

def load_repo_files(repo_path):
    documents = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java", ".cpp", ".go", ".rs", ".md")):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    documents.append({
                        "file_path": file_path,
                        "content": content
                    })

                except:
                    pass

    return documents


def list_repo_files(repo_path):

    repo_files = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):

                full_path = os.path.join(root, file)

                # convert to repo-relative path
                relative_path = os.path.relpath(full_path, repo_path)

                repo_files.append(relative_path)

    return repo_files

def load_selected_files(file_paths, repo_path):

    documents = []

    for path in file_paths:

        full_path = os.path.join(repo_path, path)

        try:
            with open(full_path, "r", encoding="utf-8") as f:

                content = f.read()

                documents.append({
                    "file_path": path,
                    "content": content
                })

        except Exception:
            pass

    return documents
