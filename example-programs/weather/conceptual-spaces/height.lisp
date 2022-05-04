(define height-concept
  (def-concept :name "height" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define height-space
  (def-conceptual-space :name "height" :parent_concept height-concept
    :no_of_dimensions 1 :is_basic_level True
    :super_space_to_coordinate_function_map
    (dict (list (tuple "temperature" (python """
lambda location: [[(c[0]-4)/1.8] for c in location.coordinates]
"""))))))
(define high-concept
  (def-concept :name "high" :locations (list (Location (list (list 10)) height-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space height-space :distance_function centroid_euclidean_distance))
(define low-concept
  (def-concept :name "low" :locations (list (Location (list (list 0)) height-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space height-space :distance_function centroid_euclidean_distance))

(def-relation :start high-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start low-concept :end less-concept :parent_concept more-concept :activation 1.0)

(define high-word
  (def-letter-chunk :name "high" :parent_space height-space
    :locations (list (Location (list (list 10)) height-space))))
(def-relation :start high-concept :end high-word :parent_concept jj-concept)
(def-relation :start high-concept :end high-word :parent_concept jjr-concept)
(def-relation :start high-word :end -er :parent_concept jjr-concept)
(define low-word
  (def-letter-chunk :name "low" :parent_space height-space
    :locations (list (Location (list (list 0)) height-space))))
(def-relation :start low-concept :end low-word :parent_concept jj-concept)
(def-relation :start low-concept :end low-word :parent_concept jjr-concept)
(def-relation :start low-word :end -er :parent_concept jjr-concept)
