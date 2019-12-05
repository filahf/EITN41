from hashlib import sha256


class MerkleNode:
    """
    Stores the hash and the parent.
    """
    def __init__(self, hash):
        self.hash = hash
        self.parent = None
        self.left_child = None
        self.right_child = None

class MerkleTree:
    """
    Stores the leaves and the root hash of the tree.
    """
    leaves = []
    def __init__(self, data_chunks):

        for chunk in data_chunks:
            node = MerkleNode(self.compute_hash(chunk))
            self.leaves.append(node)

        self.root = self.build_merkle_tree(self.leaves)

    def build_merkle_tree(self, leaves):
        """
        Builds the Merkle tree from a list of leaves. In case of an odd number of leaves, the last leaf is duplicated.
        """
        num_leaves = len(leaves)
        if num_leaves == 1:
            return leaves[0]

        parents = []

        i = 0
        while i < num_leaves:
            left_child = leaves[i]
            right_child = leaves[i + 1] if i + 1 < num_leaves else left_child

            parents.append(self.create_parent(left_child, right_child))

            i += 2

        return self.build_merkle_tree(parents)

    ###
    def create_parent(self, left_child, right_child):
        parent = MerkleNode(
            self.compute_hash(left_child.hash + right_child.hash))
        
        parent.left_child, parent.right_child = left_child, right_child
        left_child.parent, right_child.parent = parent, parent

        return parent
    ###
    

    
    def get_audit_trail(self, chunk_hash):
        """
        Checks if the leaf exists, and returns the audit trail
        in case it does.
        """
        for leaf in self.leaves:
            if leaf.hash == chunk_hash:
                print("Leaf exists")
                print(leaf.hash)
                return self.generate_audit_trail(leaf)
        return False

    def generate_audit_trail(self, merkle_node, trail=[]):
        """
        Generates the audit trail in a bottom-up fashion
        """
        if merkle_node == self.root:
            trail.append(merkle_node.hash)
            return trail

        # check if the merkle_node is the left child or the right child
        is_left = merkle_node.parent.left_child == merkle_node
        if is_left:
            # since the current node is left child, right child is
            # needed for the audit trail. We'll need this info later
            # for audit proof.
            trail.append((merkle_node.parent.right_child.hash, not is_left))
            return self.generate_audit_trail(merkle_node.parent, trail)
        else:
            trail.append((merkle_node.parent.left_child.hash, is_left))
            return self.generate_audit_trail(merkle_node.parent, trail)


    @staticmethod
    def compute_hash(data):
        data = data.encode('utf-8')
        return sha256(data).hexdigest()

file = "01234567"
chunks = list(file)
merkle_tree = MerkleTree(chunks)
print(merkle_tree.root.hash)
chunk_hash = MerkleTree.compute_hash("2")
audit_trail = merkle_tree.get_audit_trail(chunk_hash)