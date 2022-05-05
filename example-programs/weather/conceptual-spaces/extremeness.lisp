(define extremeness-concept
  (def-concept :name "extremeness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define extremeness-space
  (def-conceptual-space :name "extremeness" :parent_concept extremeness-concept
    :no_of_dimensions 1))
(define extreme-concept
  (def-concept :name "extreme" :locations (list (Location (list (list 10)) extremeness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space extremeness-space :distance_function centroid_euclidean_distance))

(define extreme-word (def-letter-chunk :name "extreme" :locations (list)))
(def-relation :start extreme-concept :end extreme-word :parent_concept jj-concept)
