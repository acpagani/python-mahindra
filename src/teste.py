import getpass

historico = {
    "1231273189":
    {
        "1":
            [
                {"role": "system", "content": "prompt1"},
                {"role": "user", "content": "mensagem"},
                {"role": "assistant", "content": "prompt2"},
                {"role": "system", "content": "prompt3"},
            ],
        "2":
        [

        ]
    }
}

index = historico.get("1231273189", '').get("1", '')[1].get("content", '')


senha = getpass.getpass()

