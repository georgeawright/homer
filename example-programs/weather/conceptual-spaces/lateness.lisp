(define lateness-concept
  (def-concept :name "lateness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define lateness-space
  (def-conceptual-space :name "lateness" :parent_concept lateness-concept
    :no_of_dimensions 1 :is_basic_level True
    :super_space_to_coordinate_function_map
    (dict (list (tuple "time" (python """
lambda location: [[(c[0]*10)/48] for c in location.coordinates]
"""))))))
(define early-concept
  (def-concept :name "early" :locations (list (Location (list (list 0)) lateness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space lateness-space :distance_function centroid_euclidean_distance))
(define late-concept
  (def-concept :name "late" :locations (list (Location (list (list 10)) lateness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space lateness-space :distance_function centroid_euclidean_distance))

(def-relation :start late-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start early-concept :end less-concept :parent_concept more-concept :activation 1.0)

(define early-word
  (def-letter-chunk :name "early" :parent_space lateness-space
    :locations (list (Location (list (list 0)) lateness-space))))
(def-relation :start early-concept :end early-word :parent_concept jj-concept)
(define earli-word
  (def-letter-chunk :name "earli" :parent_space lateness-space
    :locations (list (Location (list (list 10)) lateness-space))))
(def-relation :start early-concept :end earli-word :parent_concept jjr-concept)
(def-relation :start earli-word :end -er :parent_concept jjr-concept)
(define late-word
  (def-letter-chunk :name "late" :parent_space lateness-space
    :locations (list (Location (list (list 0)) lateness-space))))
(def-relation :start late-concept :end late-word :parent_concept jj-concept)
(define lat-word
  (def-letter-chunk :name "lat" :parent_space lateness-space
    :locations (list (Location (list (list 10)) lateness-space))))
(def-relation :start late-concept :end lat-word :parent_concept jjr-concept)
(def-relation :start lat-word :end -er :parent_concept jjr-concept)

(define same-lateness-concept (def-concept :name "same-lateness"))
(def-relation :start same-concept :end same-lateness-concept
  :parent_concept lateness-concept)
(define different-lateness-concept (def-concept :name "different-lateness"))
(def-relation :start different-concept :end different-lateness-concept
  :parent_concept lateness-concept)
(define more-lateness-concept (def-concept :name "more-lateness"))
(def-relation :start more-concept :end more-lateness-concept
  :parent_concept lateness-concept)
(define less-lateness-concept (def-concept :name "less-lateness"))
(def-relation :start less-concept :end less-lateness-concept
  :parent_concept lateness-concept)
