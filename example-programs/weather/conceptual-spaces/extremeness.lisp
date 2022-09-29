(define extremeness-concept
  (def-concept :name "extremeness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define extremeness-space
  (def-conceptual-space :name "extremeness" :parent_concept extremeness-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "temperature" (python """
lambda location: [[abs(c[0]-13)] for c in location.coordinates]
"""))))))
(define extreme-concept
  (def-concept :name "extreme" :locations (list (Location (list (list 10)) extremeness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space extremeness-space :distance_function centroid_euclidean_distance))

(define extreme-word (def-letter-chunk :name "extreme" :locations (list)))
(def-relation :start extreme-concept :end extreme-word :parent_concept jj-concept)

(define same-extremeness-concept (def-concept :name "same-extremeness"))
(def-relation :start same-concept :end same-extremeness-concept
  :parent_concept extremeness-concept)
(define different-extremeness-concept (def-concept :name "different-extremeness"))
(def-relation :start different-concept :end different-extremeness-concept
  :parent_concept extremeness-concept)
(define more-extremeness-concept (def-concept :name "more-extremeness"))
(def-relation :start more-concept :end more-extremeness-concept
  :parent_concept extremeness-concept)
(define less-extremeness-concept (def-concept :name "less-extremeness"))
(def-relation :start less-concept :end less-extremeness-concept
  :parent_concept extremeness-concept)
