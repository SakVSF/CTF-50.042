# 50.042_CTF
Team : Ivan Feng, Wang Siyang, Weihong Qiu, Dylan Raharja
- [50.042_CTF](#50042_ctf)
  - [Story](#story)
  - [Challenge](#challenge)
## Story

The boss of the company is a very stingy person who doesn't want to hire any student taking 50.042 Foundations of Cybersecurity because he thinks that he can google everything. He google and learns the implementation of RSA.

He encrypts the plaintext with a "secret cipher" first. Despite that, he does not trust that the "secret cipher" will provide sufficient defence of his plaintext. He then decides to use RSA on the ciphertext. 

However, he realises that generating a random large prime for RSA is very time consuming and sometimes non-deterministic, so to be safe, he goes to the bookstore to buy a big book of large prime numbers. Then, he uses a random number generator to select a page, which contains a unique large prime.

After trying some of the capture the flag problem from 50.042 Foundations of Cybersecurity, he decided to buy two books to prevent squaring of N since the birthday paradox problem dictate choose from the same book will have a high chance of collision.

He thought to himself that he is so smart and there is no need to hire student taking 50.042 Foundations of Cybersecurity. Can you prove him wrong?

## Challenge

To activate the challenge:

`python3 daemon_manager.py -a`

To connect to the challenge server and see it work:

`nc localhost 13370`

`{"msg": "request"}`

To Execute attack:

`python3 attack.py`
