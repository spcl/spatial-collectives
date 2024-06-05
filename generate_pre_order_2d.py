import numpy as np
import math
from collections import deque
import shutil
import argparse

tr = 2

class Vertex:

	def __init__(self, ids, tree_size, depth):
		self.id = ids
		self.tree_size = tree_size
		self.depth = depth
		self.rcv_count = 0
		self.rcv_color = 0
		self.snd_color = 0
		self.snd_control = False
		self.children = []
  
def insert_line_at(file_name, line_number, text):
    """
    Insert a line into a file at a specific line number.

    :param file_name: The name of the file to be modified.
    :param line_number: The line number at which to insert the new line (1-based index).
    :param text: The text to be inserted.
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Adjust the line number to be zero-indexed
    line_number -= 1

    # Ensure the specified line number is within the file's length
    if line_number < 0 or line_number > len(lines):
        print("Error: line number out of range")
        return

    # Insert the new line
    lines.insert(line_number, text + '\n')

    # Write the modified lines back to the file
    with open(file_name, 'w') as file:
        file.writelines(lines)
        
def insert_lines_at(file_name, line_number, lines_to_insert):
    """
    Insert multiple lines into a file at a specific line number.

    :param file_name: The name of the file to be modified.
    :param line_number: The line number at which to insert the new lines (1-based index).
    :param lines_to_insert: A list of lines to be inserted.
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Adjust the line number to be zero-indexed
    line_number -= 1

    # Ensure the specified line number is within the file's length
    if line_number < 0 or line_number > len(lines):
        print("Error: line number out of range")
        return

    # Prepare the lines to be inserted with newline characters
    lines_to_insert = [line + '\n' for line in lines_to_insert]

    # Insert the new lines
    lines[line_number:line_number] = lines_to_insert

    # Write the modified lines back to the file
    with open(file_name, 'w') as file:
        file.writelines(lines)

  
def process_pe(pe, all_pes):
  all_pes[pe.id] = pe
  pe.rcv_count = len(pe.children)
  # print(f'id: {pe.id}, rcv count: {pe.rcv_count}, snd color: {pe.snd_color}, rcv color: {pe.rcv_color}')
  if (len(pe.children) == 0):	
    return
  for child in pe.children:
    child.snd_color = pe.rcv_color
    child.rcv_color = pe.snd_color
  pe.children[-1].snd_control = True

  for child in pe.children:
    process_pe(child, all_pes)

def lower_bound(P, B, dir):
  dp = np.array([[np.inf for _ in range(P + 1)] for _ in range(P + 1)])
  # minimum energy to reduce a scalar for (pes, depth)
  dp[0, :] = 0
  dp[1, :] = 0

  for receiver in range(2, P + 1):
    for d in range(1, P + 1):
      dp[receiver, d] = dp[receiver, d-1]
      for sender in range(1, receiver):
        dp[receiver, d] = min(dp[receiver, d], dp[sender, d - 1] + dp[receiver - sender, d] + receiver - sender)
      
      
  dp_copied = np.array(dp[P], copy=True)
  for d in range(P + 1):
    dp_copied[d] = (B * dp_copied[d])/max(1, P - 1) + P - 1 + d * (2 * tr + 1)
  cur_d = np.argmin(dp_copied)

  root = Vertex(0, P, cur_d)
  root.snd_control = 0
  root.rcv_color = 1
  pes = deque()
  pes.append(root)

  while pes:
    pe = pes.popleft()
    while (pe.tree_size > 1):
      for sender in range(1, pe.tree_size):
        if (dp[pe.tree_size, pe.depth] == dp[sender, pe.depth - 1] + dp[pe.tree_size - sender, pe.depth] + pe.tree_size - sender):
          sender_vertex = Vertex(pe.id + pe.tree_size - sender, sender, pe.depth - 1)
          pe.children.append(sender_vertex)
          pe.tree_size -= sender
          pes.append(sender_vertex)
          break
    pe.children.reverse()

  all_pes = [None for i in range(P)]
  process_pe(root, all_pes)
  total_lines = []
  new_file_name = 'modules/pre_order_runtime.csl'
  shutil.copy("modules/pre_order_runtime_base.csl", new_file_name)
  for i in range(P):
    pe = all_pes[i]
    out_color =  "color_1" if (pe.snd_color == 0) else "color_2"
    in_color =  "color_2" if (pe.snd_color == 0) else "color_1"
    snd_control =  "true" if (pe.snd_control) else "false"
    out_color_line = '    out_color = {};'.format(out_color)
    in_color_line = '   in_color = {};'.format(in_color)
    rcv_count_line = '    rcv_cnt = {};'.format(pe.rcv_count)
    snd_control_line = '    is_ctrl = {};'.format(snd_control)
    if_line = ' if (pe_id == {}) '.format(i) + '{'
    end_if_line = ' }'
    total_lines += [if_line, out_color_line, in_color_line, rcv_count_line, snd_control_line, end_if_line]
  insert_lines_at(new_file_name, 60, total_lines)

def main():
    parser = argparse.ArgumentParser(description="Greet two people by their names.")
    parser.add_argument("P", type=int, help="Number of PEs")
    parser.add_argument("B", type=int, help="Vector Length")
    parser.add_argument("dir", type=str, help="direction")
    args = parser.parse_args()

    lower_bound(args.P, args.B, args.dir)

if __name__ == "__main__":
    main()
