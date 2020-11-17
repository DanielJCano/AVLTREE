class nodo:
    def __init__(self, value = None):
      self.value = value
      self.left = None
      self.right = None
      self.parent = None
      self.height = 1

class AVLTree:
      def __init__(self):
            self.root = None

      # Se encarga de arreglar el arbol para imprimirlo
      def __repr__(self):
            if self.root == None: return ''
            content = "\n"                                                                      # mantiene el ultimo hilo
            cur_nodos = [self.root]
            cur_height = self.root.height
            sep = ' ' *(2**(cur_height - 1))
            while True:
                  cur_height += -1
                  if len(cur_nodos) == 0: break
                  cur_row = " "
                  next_row = " "
                  next_nodos = [ ]

                  if all (n is None for n in cur_nodos):
                        break

                  for n in cur_nodos:

                        if n == None:
                              cur_row += '   ' + sep
                              next_row += '   ' + sep
                              next_nodos.extend([None, None])
                              continue
                        if n.value != None:
                              buf = ' ' * int((5-len(str(n.value)))/2)
                              cur_row += '%s%s%s' %(buf,str(n.value),buf) + sep
                        else:
                              cur_row += ' ' + sep
                        if n.left != None:
                              next_nodos.append(n.left)
                              next_row += ' /' + sep
                        else:
                              next_row += '  ' + sep
                              next_nodos.append(None)
                        if n.right != None:
                              next_nodos.append(n.right)
                              next_row += '\ ' + sep
                        else:
                              next_row += '  ' + sep
                              next_nodos.append(None)

                  content += (cur_height*'   '+cur_row+'\n'+cur_height*'   ' + next_row + '\n')
                  cur_nodos = next_nodos
                  sep = ' '*int(len(sep)/2)                                                     # corta las separaciones a la mitad
            return content


      def insert(self, value):
            if self.root == None:
                  self.root = nodo(value)
            else:
                  self._insert(value, self.root)

      def _insert(self, value, cur_nodo):                                                       # Se encarga de incertar el nodo en el lugar correcto
                  if value < cur_nodo.value:
                        if cur_nodo.left == None:
                              cur_nodo.left = nodo(value)
                              cur_nodo.left.parent = cur_nodo
                              self._inspect_insertion(cur_nodo.left)
                        else:
                              self._insert(value, cur_nodo.left)
                  elif value > cur_nodo.value:
                        if cur_nodo.right == None:
                              cur_nodo.right = nodo(value)
                              cur_nodo.right.parent = cur_nodo
                              self._inspect_insertion(cur_nodo.right)
                        else:
                              self._insert(value, cur_nodo.right)
                  else:
                        print("El valor ya esta en el arbol.")

      def print_tree(self):
            if self.root != None:
                  self._print_tree(self.root)



      def _print_tree(self, cur_nodo):
            if cur_nodo != None:
                  self._print_tree(cur_nodo.left)
                  print('%s, h=%d'%(str(cur_nodo.value), cur_nodo.height))
                  self._print_tree(cur_nodo.right)



      def height(self):
            if self.root != None:
                  return self._height(self.root, 0)
            else:
                  return 0

      def _height(self, cur_nodo, cur_height):
            if cur_nodo == None: return cur_height
            left_height = self._height(cur_nodo.left, cur_height + 1)
            right_height = self._height(cur_nodo.right, cur_height +1)
            return max(left_height, right_height)

      def find(self, value):
            if self.root != None:
                  return self._find(value, self.root)
            else:
                  return None

      def _find(self, value, cur_nodo):
            if value == cur_nodo.value:
                  return cur_nodo
            elif value < cur_nodo.value and cur_nodo.left != None:
                  return self._find(value,cur_nodo.left)
            elif value > cur_nodo.value and cur_nodo.left != None:
                  return self._find(value, cur_nodo.right)

      def delete_value(self, value):
            return self.delete_nodo(self.find(value))

      def delete_nodo(self, nodo):

            if nodo == None or self.find(nodo.value) == None:                                   # Protege que no trate de borrar un nodo no existente
                  print("\nEl nodo que quieres borrar no esta en el arbol.")
                  return None                                                                   # devuelve el nodo con el valor mínimo en el árbol arraigado en el nodo de entrada

            def min_value_nodo(n):                                                              # regresa el nodo con el valor mas pequeño dentro del arbol
                  current = n
                  while current.left != None:
                        current = current.left
                  return current

            def num_children(n):                                                                # regresa los nodos hijos del nodo padre especificado
                  num_children = 0
                  if n.left != None: num_children += 1
                  if n.right != None: num_children += 1
                  return num_children

            nodo_parent = nodo.parent                                                           # Consigue el nodo padre del nodo a borrar

            nodo_children = num_children(nodo)                                                  # Consigue el numero de hijos del nodo a borrar

            # Analiza varios casos del arbol y nodos a borrar
            # PRIMER CASO: cuando el nodo a borrar no tiene hijos.
            if nodo_children == 0:
                  if nodo_parent != None:                                                       # remueve la referencia del nodo padre
                        if nodo_parent.left == nodo:
                              nodo_parent.left == None
                        else:
                              nodo_parent.right = None
                  else:
                        self.root = None

            # SEGUNDO CASO: cuando el nodo a borrar solo tiene un hijo.
            if nodo_children == 1:

                  if nodo.left != None:                                                         # agarra el nodo con solo un hijo
                        child = nodo.left
                  else:
                        child = nodo.right

                  if nodo_parent != None:                                                       # remplaca el nodo que tiene que ser borrado con su hijo
                        if nodo_parent.left == nodo:
                              nodo_parent.right = child 
                        else:
                              child = nodo.right

                        if nodo_parent != None:                                                 # Remplaca el nodo a a borrar con su hijo
                              if nodo_parent.left == nodo:
                                    nodo_parent.left = child

                              else:
                                    nodo_parent.right = child

                        else:
                              self.root = child

                        child.parent = nodo_parent                                              # correcciona el apuntador padre en el nodo

                  # TERCER CASO: si el nodo tiene dos hijos.
                  if nodo_children == 2:
                        successor = min_value_nodo(nodo.right)                                  # Agarra el succesor del nodo borrado en froma inorder

                        nodo.value = successor.value                                            # copia el valor del hijo del nodo borrado y lo copia al nodo padre

                        self.delete_nodo(successor)                                             # elimina el hijo copiado ya que ya fue transferido a otro nodo

                        return                                                                  # se sale de la funcion para no llamar dos veces la funcion inspect_deletion

                  if nodo_parent != None:                                                       # Arregla la altura del padre del nodo en cuestion
                        nodo_parent.height = 1 + max(self.get_height(nodo_parent.left), self.get_height(nodo_parent.right))

                        self._inspect_deletion(nodo_parent)                                     # Hace un recorrido del arbol para checar que ninguna regla AVL no se haya cumplido

      def search(self,value):
            if self.root != None:
                  return self._search(value, self.root)

            else:
                  return False

      def _search(self, value, cur_nodo):
            if value == cur_nodo.value:
                  return True
            elif value < cur_nodo.value and cur_nodo.left != None:
                  return self._search(value, cur_nodo.left)

            elif value > cur_nodo.value and cur_nodo.right != None:
                  return self._search(value, cur_nodo.right)

            return False

      def _inspect_insertion(self, cur_nodo, path = []):
            if cur_nodo.parent == None: return
            path = [cur_nodo] + path

            left_height = self.get_height(cur_nodo.parent.left)
            right_height = self.get_height(cur_nodo.parent.right)

            print("Altura izquierda y derecha.", left_height, right_height)

            if abs(left_height - right_height) > 1:
                  print("Path: ", path[0].value)
                  path = [cur_nodo.parent] + path
                  print("Path 2:", path[0].value, path[1].value, path[2].value)
                  self._rebalance_nodo(path[0], path[1], path[2])
                  return

            new_height = 1 + cur_nodo.height
            if new_height > cur_nodo.parent.height:
                  cur_nodo.parent.height = new_height

            self._inspect_insertion(cur_nodo.parent, path)

      def _inspect_deletion(self, cur_nodo):                                                    # Revisa que el cur_nodo sea conocido
            if cur_nodo == None: return

            left_height = self.get_height(cur_nodo.left)                                        # Se crea una variable para cargar la altura de nodo hijo izquierdo
            right_height = self.get_height(cur_nodo.right)                                      # Se crea una variable para cargar la altura de nodo hijo derecho

            if abs(left_height - right_height) > 1:                                             # Se checa la diferencia entre las dos alturas para saber si esta balanciado
                  y = self.taller_child(cur_nodo)
                  x = self.taller_child(y)
                  self._rebalance_deletion(cur_nodo, y, x)                                     # Se llama la funcion de rebalanceo
            self._inspect_deletion(cur_nodo.parent)                                            # Se llama la funcion _inspect_deletion recorsivamente pasando el padre de cur_nodo como el nuevo cur_nodo


      def _rebalance_nodo(self, z, y, x):
                  if y == z.left and x == y.left:                                              # Si es el caso "left left" 
                        self._right_rotate(z)                                                  # se hace una rotacion a la derecha del nodo Z

                  elif y == z.left and x == y.right:                                           # Si es el caso "Left Right"
                        self._left_rotate(y)                                                   # se hace una rotacion a la izquierda del nodo Y
                        self._right_rotate(z)                                                  # se hace una rotacion a la derecha del nodo Z

                  elif y == z.right and x == y.right:                                          # Si es el caso "Right Right"
                        self._left_rotate(z)                                                   # se hace una rotacion a la izquierda del nodo Z

                  elif y == z.right and x == y.left:                                           # Si es el caso de "Right Left"
                        self._right_rotate(y)                                                  # se hace una rotacion a la derecha del nodo Y
                        self._left_rotate(z)                                                   # se hace una rotacion a la izquierda del nodo Z

                  else:
                        raise Exception("_rebalance_nodo: z, y, x: la configuracion de nodo no reconocido!")      # Indica que ha un problema con la estructura del arbol

      def _right_rotate(self, z):                                                               # Hace la rotacion a la derecha
                  sub_root = z.parent
                  y = z.left
                  t3 = y.right
                  y.right_child = z
                  z.parent = y
                  z.left = t3
                  if t3 != None: t3.parent = z
                  y.parent = sub_root
                  if y.parent == None:
                        self.root = y
                  else:
                        if y.parent.left == z:
                              y.parent.left = y
                        else:
                              y.parent.right = y

                  z.height = 1 + max(self.get_height(z.left), self.get_height(y.right))         # Se actualiza la altura de Z

                  y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))         # Se actualiza la altura de Y

      def _left_rotate(self, z):                                                                # Hace la rotacion a la izquierda
                  sub_root = z.parent
                  y = z.right
                  t2 = y.left
                  y.left = z
                  z.parent = y
                  z.right = t2
                  if t2 != None: t2.parent = z
                  y.parent = sub_root
                  if y.parent == None:
                        self.root = y
                  else:
                        if y.parent.left == z:
                              y.parent.left = y
                        else:
                              y.parent.right = y
                  z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))         # Se actualiza la altura de Z
                  y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))         # Se actualiza la altura de Y

      def get_height(self, cur_nodo):
            if cur_nodo == None: return 0
            return cur_nodo.height

      def taller_child(self, cur_nodo):
            left = self.get_height(cur_nodo.left)                                               # Se obtiene la altura del hijo izquierdo
            right = self.get_height(cur_nodo.right)                                             # Se obtiene la altura del hijo derecho
            return cur_nodo.left if left >= right else cur_nodo.right                           # Regresa el mas alto de los dos nodos hijos

if __name__ == "__main__":
      Tree = AVLTree()
      for i in range(10):
            Tree.insert(i)
            print(Tree)

      print("*****************************************")

      for i in range(0,5):
            Tree.delete_value(i)
            print(Tree)

      print(Tree)
      print("\n DANIEL JARA CANO 23052")
      print("\n")