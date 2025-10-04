# Updated Blocsym.py - Integrated Key Moshing, Dojos Tie-In
# AGPL-3.0 licensed. -- OliviaLynnArchive fork, 2025
# Main monoscript with key moshing for trustless queues, calm/dream features.
# Ties to db_utils for cross-chain, entropy checks; calls dojo_train for hidden updates.
# Fixed bytes literal for 'ÿ' using encode('utf-8').

import os
import sys
import time
import zlib
import json
import hashlib
import logging
import signal
import threading
import multiprocessing
from collections import defaultdict, deque
from queue import Queue
import numpy as np
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import random  # For dream generative
from math import sin  # For curve gradation

# Import db_utils for dojo/cross-chain integration
from db_utils import BlocsymDB, SCENERY_DESCS  # Reuse calm scenery

# Blockchain libraries (placeholders, import as needed)
# from bitcoinlib.wallets import Wallet
# from web3 import Web3
# from solana.rpc.api import Client as SolanaClient
# from solana.keypair import Keypair
# from solana.transaction import Transaction
# from solana.system_program import transfer as sol_transfer

# Global Defaults
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BUFFER_SIZE = 256
CYCLE_LIMIT = 144
NODES = 8
GLOBAL_TIMEOUT = 300
HASH_COUNT = 60
WEI_PER_HASH = 8
GOSSIP_STATUS = "idle"
TRANSACTION_BUFFER_SIZE = 1024
ANIMATION_SPEED = 1
PRUNE_AFTER = 2141
HASH_WINDOW_MIN = 3
HASH_WINDOW_MAX = 145
SIDE_HASHES = 42
CONSENSUS_THRESHOLD = 0.69
KAPPA_BASE = 0.3536
ROCK_DOTS = "ÿÿÿ".encode('utf-8')  # Fixed for bytes

main_exit_flag = False

def handle_exit(sig, frame):
    global main_exit_flag
    print("\n[Signal] Caught => Setting exit flag.")
    main_exit_flag = True

# Function Registry
FUNCTION_REGISTRY = {}

def register_function(func_id, compressed_bytes=None):
    def decorator(func):
        FUNCTION_REGISTRY[func_id] = {"function": func, "bytes": compressed_bytes}
        return func
    return decorator

def execute_function_string(func_id: str, *args, **kwargs):
    entry = FUNCTION_REGISTRY.get(func_id)
    if entry:
        func = entry["function"]
        logger.info(f"Executing function ID {func_id} from registry...")
        return func(*args, **kwargs)
    logger.warning(f"No function found for ID: {func_id}")
    return None

# Key Mosher Class (updated with db/dojo tie)
class KeyMosher:
    def __init__(self, queue_size=1024, db_path='blocsym.db'):
        self.queue = deque(maxlen=queue_size)
        self.block_height = 0
        self.hash_height = 0
        self.prune_buffer = deque(maxlen=PRUNE_AFTER)
        self.db = BlocsymDB(db_path)  # Tie to db for persistent states
        self.afk_timer = time.time()
        self.meditation_active = False

    def mosh_key(self, key, hash_str):
        """Mosh key with hash: Prefix block height, suffix next hash, XOR blend."""
        prefixed = f"{self.block_height}:{key}"
        suffixed = f"{prefixed}:{self.hash_height}"
        moshed = ""
        for i in range(len(suffixed)):
            moshed += chr(ord(suffixed[i]) ^ ord(hash_str[i % len(hash_str)]))
        self.queue.append(moshed)
        self.prune_buffer.append(moshed)
        self.update_heights()
        self.meditate_if_afk()
        # Dojo train moshed for hidden update
        trained = self.db.dojo_train(moshed)
        logger.info(trained)
        return moshed

    def update_heights(self):
        """Update block/hash heights, prune if needed."""
        self.block_height += 1
        self.hash_height = int(hashlib.sha256(str(self.block_height).encode()).hexdigest(), 16) % 1000000
        if len(self.prune_buffer) >= PRUNE_AFTER:
            self.prune_old()

    def prune_old(self):
        """Prune old hashes, check window."""
        for _ in range(HASH_WINDOW_MIN):
            if len(self.prune_buffer) > HASH_WINDOW_MAX:
                self.prune_buffer.popleft()
        # Dream generative prune: Random recurv add if low entropy
        if random.random() < 0.3:  # Dream chance
            dream_hash = ''.join(random.choice('abcdef0123456789') for _ in range(8))
            self.prune_buffer.append(dream_hash)  # Dream insert

    def check_consensus(self, nodes=NODES):
        """69% consensus check."""
        votes = random.randint(0, nodes)  # Sim
        return votes / nodes >= CONSENSUS_THRESHOLD

    def curve_gradation(self, data):
        """Smooth gradation via sin interp."""
        grad = sin(len(data)) * 0.5 + 0.5
        return data[:int(len(data) * grad)]

    def thought_fork(self, data):
        """Fork thoughts: Branch reverse/upper."""
        fork1 = data[::-1]
        fork2 = data.upper()
        return fork1 if len(data) % 2 == 0 else fork2

    def recurvature(self, data, depth=3):
        """Recursive bow nesting."""
        if depth == 0:
            return data
        return self.recurvature(data + ' recurv', depth-1)

    def dojo_train(self, updates):
        """Call db dojo for hidden training."""
        return self.db.dojo_train(self.recurvature(self.thought_fork(self.curve_gradation(updates))))

    def meditate_if_afk(self):
        """Calm meditation if AFK >60s."""
        if time.time() - self.afk_timer > 60 and not self.meditation_active:
            self.meditation_active = True
            scenery = random.choice(SCENERY_DESCS)
            logger.info(f"[Blocsÿm Meditates]: {scenery}")
        elif time.time() - self.afk_timer < 60:
            self.meditation_active = False

    def close(self):
        self.db.close()

# BFS Chunking (tie to moshing)
def chunk_file_into_bfs_nodes(file_path, chunk_size=1024):
    adjacency_dict = {}
    node_data = {}
    with open(file_path, 'rb') as f:
        i = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            node_id = f"chunk_{i}"
            node_data[node_id] = chunk
            adjacency_dict[node_id] = [f"chunk_{i+1}"]
            i += 1
        if i > 0:
            adjacency_dict[f"chunk_{i-1}"] = []
    return adjacency_dict, node_data

@register_function('BFS')
def handle_bfs_chunking_demo(file_path, chunk_size=256):
    adjacency_dict, node_data = chunk_file_into_bfs_nodes(file_path, chunk_size)
    # Mosh node IDs
    mosher = KeyMosher()
    for node in node_data:
        mosher.mosh_key(node, hashlib.sha256(node_data[node]).hexdigest())
    return {"status": "BFS complete with moshing", "chunks": len(node_data)}

# Ephemeral Bastion (add dojo tie)
class EphemeralBastion:
    def __init__(self, ephemeral_key=None):
        if ephemeral_key is None:
            ephemeral_key = Fernet.generate_key()
        self.ephemeral_key = ephemeral_key
        self.cipher_suite = Fernet(self.ephemeral_key)

    def transform_inbound(self, inbound_bytes: bytes) -> bytes:
        return self.cipher_suite.encrypt(inbound_bytes)

    def transform_outbound(self, inbound_bytes: bytes) -> bytes:
        plaintext = self.cipher_suite.decrypt(inbound_bytes)
        return self.cipher_suite.encrypt(plaintext)

@register_function('BASTION')
def multi_bastion_demo(data_str: str, bastion_count=3):
    data_bytes = data_str.encode('utf-8')
    bastions = [EphemeralBastion() for _ in range(bastion_count)]
    current = data_bytes
    for bastion in bastions:
        current = bastion.transform_inbound(current)
    # Dojo train on transformed
    mosher = KeyMosher()
    trained = mosher.dojo_train(current.decode('utf-8'))
    return {"status": "Bastion complete", "final_output": trained}

# Main CLI Loop with Moshing
def main_cli_loop():
    mosher = KeyMosher()
    while not main_exit_flag:
        print("[Main CLI] Idle... Enter key to mosh (or Ctrl+C to exit):")
        try:
            input_key = input().strip()
            if input_key:
                hash_str = hashlib.sha256(input_key.encode()).hexdigest()
                moshed = mosher.mosh_key(input_key, hash_str)
                print(f"Moshed: {moshed}")
        except EOFError:
            break
        time.sleep(2)  # Idle check

# Flask App
app = Flask(__name__)
socketio = SocketIO(app)

# Placeholder endpoints
@app.route("/metrics/block_height", methods=["GET"])
def get_block_height_api():
    return jsonify({"block_height": 0})  # Sim

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        print("[Main] Starting Flask + SocketIO server on port 5000...")
        socketio.run(app, host="0.0.0.0", port=5000)
    else:
        print("[Main] Starting CLI demonstration. Use Ctrl+C to exit, or run with 'server' arg for Flask.")
        try:
            main_cli_loop()
        except KeyboardInterrupt:
            pass
        finally:
            print("[Main] Exiting gracefully.")
