# Based on https://www.codementor.io/blog/merkle-trees-5h9arzd3n8

from hashlib import sha1
#Treat leaves in the tree as Nodes
class MerkleNode:
    def __init__(self, hash):
        self.hash = hash
        self.parent = None
        self.left_child = None
        self.right_child = None

class MerkleTree:
   leaves = []
   def __init__(self, data):
      for x in data:
         node = MerkleNode(x)
         self.leaves.append(node)

      self.root = self.build_merkle_tree(self.leaves)

   def build_merkle_tree(self, leaves):
        num_leaves = len(leaves)
        if num_leaves == 1:
            return leaves[0]

        parents = []

        i = 0
        #Itterate over the leaves and create parents with 2 childrens each
        while i < num_leaves:
            left_child = leaves[i]
            #If the list is uneven the left child will be duplicated and assigned as twins
            right_child = leaves[i + 1] if i + 1 < num_leaves else left_child

            parents.append(self.create_parent_node(left_child, right_child))

            i += 2

        return self.build_merkle_tree(parents)
    #Create a parent node with hash value H(H(LC)+H(RC)). Link the children to newly created parent node
   def create_parent_node(self, left_child, right_child):
        parent = MerkleNode(self.compute_hash(left_child.hash + right_child.hash))
        
        parent.left_child = left_child
        parent.right_child = right_child
        left_child.parent = parent
        right_child.parent = parent

        return parent
    #check if the target node is in the tree. If true generate the path
   def get_path(self, chunk_hash):
        for leaf in self.leaves:
            if leaf.hash == chunk_hash:
                return self.generate_path(leaf)
        return False
    # Generate path bottom up
   def generate_path(self, merkle_node, trail=[]):
        if merkle_node == self.root:
            trail.append(merkle_node.hash)
            return trail
        #check direction in the path
        is_left = merkle_node.parent.left_child == merkle_node
        if is_left:
            trail.append(("R"+merkle_node.parent.right_child.hash))
            return self.generate_path(merkle_node.parent, trail)
        else:
            trail.append(("L"+merkle_node.parent.left_child.hash))
            return self.generate_path(merkle_node.parent, trail)

   @staticmethod
   def compute_hash(data):
        return sha1(bytearray.fromhex(data)).hexdigest()


def main():
    string_list = []
    with open('HA1B/3/merkle_test2.txt', 'r', encoding='utf-8') as file:
        content = file.read().splitlines()
        for line in content:
            string_list.append(line)
    index_i = string_list.pop(0)
    index_j = string_list.pop(0)
    merkle_tree = MerkleTree(string_list)
    nodeI = string_list[int(index_i)]
    path = merkle_tree.get_path(nodeI)
    path = path[::-1]
    print(path[int(index_j)] + path[0])

if __name__ == "__main__":
    main()