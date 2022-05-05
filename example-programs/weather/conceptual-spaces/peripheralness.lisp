(define peripheralness-concept
  (def-concept :name "peripheralness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define peripheralness-space
  (def-conceptual-space :name "peripheralness" :parent_concept peripheralness-concept
    :no_of_dimensions 1))
(define peripheral-concept
  (def-concept :name "peripheral"
    :locations (list (Location (list (list 10)) peripheralness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space peripheralness-space :distance_function centroid_euclidean_distance))

(define peripheries-word (def-letter-chunk :name "peripheries" :locations (list)))
(def-relation :start peripheral-concept :end peripheries-word :parent_concept nn-concept)
