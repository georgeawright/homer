(define oppositeness-concept
  (def-concept :name "oppositeness" :locations (list) :classifier None :instance_type None
    :structure_type Relation :parent_space None
    :distance_function centroid_euclidean_distance))
(define oppositeness-space
  (def-conceptual-space :name "oppositeness" :parent_concept oppositeness-concept
    :no_of_dimensions 1))
(define opposite-concept
  (def-concept :name "opposite"
    :locations (list (Location (list (list 10)) oppositeness-space))
    :classifier (AbstractRelationClassifier) :instance_type Chunk :structure_type Relation
    :parent_space oppositeness-space :distance_function centroid_euclidean_distance))

