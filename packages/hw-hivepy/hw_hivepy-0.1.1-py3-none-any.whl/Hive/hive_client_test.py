def main() -> None:
    """Main function."""
    auth = {
        'server': 'http://192.168.31.78',
        'username': 'root@ro.ot',
        'password': '65Beforeth!',
        'proxy': 'http://127.0.0.1:8080',
    }

    hive: Hive = Hive().connect(**auth)
    project_id = '5c188d0f-f854-4030-8b98-01ace06b1fc8'
    issue_id = '506f96b1-ef33-4881-9a18-799cd8c5b3f0'
    # print(hive.get_projects())
    # print(hive.get_issues('5c188d0f-f854-4030-8b98-01ace06b1fc8'))
    # print(hive.get_file('5c188d0f-f854-4030-8b98-01ace06b1fc8', '4f03056c-cfa6-4092-94cb-625b5a17e82c'))
    hive.update_issue(project_id, issue_id, status='retest_required')
    # print(hive.get_project('5c188d0f-f854-4030-8b98-01ace06b1fc8'))
    # pprint(hive.get_projects(), indent=4)
    # project_dict: Dict = json.load(open('project.json', 'r', encoding='utf-8'))
    # project: Project = Project(**project_dict)
    # print(project)


if __name__ == "__main__":
    main()
