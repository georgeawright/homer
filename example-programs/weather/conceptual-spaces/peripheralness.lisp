(define peripheralness-concept
  (def-concept :name "peripheralness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define peripheralness-space
  (def-conceptual-space :name "peripheralness" :parent_concept peripheralness-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[((c[0]-4)**2 + (c[1]-4)**2)/2] for c in location.coordinates]
"""))))))
(define peripheral-concept
  (def-concept :name "peripheral"
    :locations (list (Location (list (list 10)) peripheralness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space peripheralness-space :distance_function centroid_euclidean_distance))

(define peripheries-word (def-letter-chunk :name "peripheries" :locations (list)))
(def-relation :start peripheral-concept :end peripheries-word :parent_concept nn-concept)

(define same-peripheralness-concept (def-concept :name "same-peripheralness"))
(def-relation :start same-concept :end same-peripheralness-concept
  :parent_concept peripheralness-concept)
(define different-peripheralness-concept (def-concept :name "different-peripheralness"))
(def-relation :start different-concept :end different-peripheralness-concept
  :parent_concept peripheralness-concept)
(define more-peripheralness-concept (def-concept :name "more-peripheralness"))
(def-relation :start more-concept :end more-peripheralness-concept
  :parent_concept peripheralness-concept)
(define less-peripheralness-concept (def-concept :name "less-peripheralness"))
(def-relation :start less-concept :end less-peripheralness-concept
  :parent_concept peripheralness-concept)
