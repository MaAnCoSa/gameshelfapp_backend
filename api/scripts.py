CREATE_USER = '''
    INSERT INTO users.users (
        username,
        no_of_games
    ) VALUES (%s, %s)
    RETURNING id, username, no_of_games
'''