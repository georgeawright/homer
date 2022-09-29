(define goodness-concept
  (def-concept :name "goodness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define goodness-space
  (def-conceptual-space :name "goodness" :parent_concept goodness-concept
    :no_of_dimensions 1 :is_basic_level True
    :super_space_to_coordinate_function_map
    (dict (list (tuple "temperature" (python """
lambda location: [[(c[0]-4)/1.8] for c in location.coordinates]
"""))))))
(define good-concept
  (def-concept :name "good" :locations (list (Location (list (list 10)) goodness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space goodness-space :distance_function centroid_euclidean_distance))
(define bad-concept
  (def-concept :name "bad" :locations (list (Location (list (list 0)) goodness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space goodness-space :distance_function centroid_euclidean_distance))

(def-relation :start good-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start bad-concept :end less-concept :parent_concept more-concept :activation 1.0)

(define good-word
  (def-letter-chunk :name "good" :parent_space goodness-space
    :locations (list (Location (list (list 10)) goodness-space))))
(def-relation :start good-concept :end good-word :parent_concept jj-concept)
(define bett-word
  (def-letter-chunk :name "bett" :parent_space goodness-space
    :locations (list (Location (list (list 10)) goodness-space))))
(def-relation :start good-concept :end bett-word :parent_concept jjr-concept)
(def-relation :start bett-word :end -er :parent_concept jjr-concept)
(define bad-word
  (def-letter-chunk :name "bad" :parent_space goodness-space
    :locations (list (Location (list (list 0)) goodness-space))))
(def-relation :start bad-concept :end bad-word :parent_concept jj-concept)
(define worse-word
  (def-letter-chunk :name "worse" :parent_space goodness-space
    :locations (list (Location (list (list 0)) goodness-space))))
(def-relation :start bad-concept :end worse-word :parent_concept jjr-concept)
(def-relation :start worse-word :end null :parent_concept jjr-concept)

(define same-goodness-concept (def-concept :name "same-goodness"))
(def-relation :start same-concept :end same-goodness-concept
  :parent_concept goodness-concept)
(define different-goodness-concept (def-concept :name "different-goodness"))
(def-relation :start different-concept :end different-goodness-concept
  :parent_concept goodness-concept)
(define more-goodness-concept (def-concept :name "more-goodness"))
(def-relation :start more-concept :end more-goodness-concept
  :parent_concept goodness-concept)
(define less-goodness-concept (def-concept :name "less-goodness"))
(def-relation :start less-concept :end less-goodness-concept
  :parent_concept goodness-concept)
