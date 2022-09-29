(define magnitude-concept
  (def-concept :name "magnitude" :locations (list) :classifier None :instance_type Link
    :structure_type None :parent_space None
    :distance_function centroid_euclidean_distance))
(define magnitude-space
  (def-conceptual-space :name "magnitude" :parent_concept magnitude-concept
    :no_of_dimensions 1 :is_basic_level True))
(define extremely-concept
  (def-concept :name "extremely"
    :locations (list (Location (list (list 2)) magnitude-space))
    :classifier (ProximityClassifier) :instance_type Link :structure_type Label
    :parent_space magnitude-space :distance_function centroid_euclidean_distance))
(define very-concept
  (def-concept :name "very"
    :locations (list (Location (list (list 1)) magnitude-space))
    :classifier (ProximityClassifier) :instance_type Link :structure_type Label
    :parent_space magnitude-space :distance_function centroid_euclidean_distance))
(define quite-concept
  (def-concept :name "quite"
    :locations (list (Location (list (list -1)) magnitude-space))
    :classifier (ProximityClassifier) :instance_type Link :structure_type Label
    :parent_space magnitude-space :distance_function centroid_euclidean_distance))
(define bit-concept
  (def-concept :name "bit"
    :locations (list (Location (list (list -2)) magnitude-space))
    :classifier (ProximityClassifier) :instance_type Link :structure_type Label
    :parent_space magnitude-space :distance_function centroid_euclidean_distance))

(define extremely-word
  (def-letter-chunk :name "extremely" :parent_space magnitude-space
    :locations (list (Location (list (list 2)) magnitude-space))))
(def-relation :start extremely-concept :end extremely-word :parent_concept rb-concept)
(define very-word
  (def-letter-chunk :name "very" :parent_space magnitude-space
    :locations (list (Location (list (list 1)) magnitude-space))))
(def-relation :start very-concept :end very-word :parent_concept rb-concept)
(define quite-word
  (def-letter-chunk :name "quite" :parent_space magnitude-space
    :locations (list (Location (list (list -1)) magnitude-space))))
(def-relation :start quite-concept :end quite-word :parent_concept rb-concept)
(define bit-word
  (def-letter-chunk :name """a bit""" :parent_space magnitude-space
    :locations (list (Location (list (list -2)) magnitude-space))))
(def-relation :start bit-concept :end bit-word :parent_concept rb-concept)

(define same-magnitude-concept (def-concept :name "same-magnitude"))
(def-relation :start same-concept :end same-magnitude-concept
  :parent_concept magnitude-concept)
(define different-magnitude-concept (def-concept :name "different-magnitude"))
(def-relation :start different-concept :end different-magnitude-concept
  :parent_concept magnitude-concept)
(define more-magnitude-concept (def-concept :name "more-magnitude"))
(def-relation :start more-concept :end more-magnitude-concept
  :parent_concept magnitude-concept)
(define less-magnitude-concept (def-concept :name "less-magnitude"))
(def-relation :start less-concept :end less-magnitude-concept
  :parent_concept magnitude-concept)
