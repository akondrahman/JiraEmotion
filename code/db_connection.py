def giveConnection():
    import pymysql.cursors
    codealike_host = "localhost"
    codealike_user = "arahman"
    codealike_password = "Ansible#2016"
    codealike_database = "emotion_in_jira"
    # Connect to the database
    codealike_connection = pymysql.connect(host=codealike_host,
                                 user=codealike_user,
                                 password=codealike_password,
                                 db=codealike_database,
                                 cursorclass=pymysql.cursors.DictCursor)
    return codealike_connection
