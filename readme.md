# Braden Eichmeier's Journal

This repository will act as both a journal and testbed for me. It's so easy to go along without contemplating one's thoughts, opinions and views on life. I belive the best version of anybody is acheived through thoughtful reflection, introspection, aspiration, and planning. As such, I want to have a location where I can place these thoughts anywhere I may be. I could do this through a GoogleDoc, or other online service, but I want to tailor my journal to what I need without jumping through the complications and restrictions of any given service. Furthermore, I hope to use this repository as a playground for several technical skills.

Though I could make all of this information private, that defeats the purpose of making it widely accessible to me. To maintain privacy, I setup a toy encryption scheme to obfuscate my thoughts. The algorithm, given in encrption.py, encrypts and decrypts all of the entries according to a password set in password.password. I will push the original file up as TestPassword, but will ignore future changes to that file. Upon pulling the repo, decrypt the folder using encryption.py. When pushing to the repo, encrypt the folder using encryption.py.

To ignore changes to your password file, you may need to run this command:

```
git update-index --skip-worktree password.password
```

To encrypt: 
```
encryption.py
```

To decrypt:
```
encryption.py 0
```

## Current Status

- The basic encryption scheme is complete

## TODO

- Design webpage
- Setup webpage to run on eichmeierbr.github.io