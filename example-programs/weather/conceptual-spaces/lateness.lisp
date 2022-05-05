(define lateness-concept
  (def-concept :name "lateness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define lateness-space
  (def-conceptual-space :name "lateness" :parent_concept lateness-concept
    :no_of_dimensions 1 :is_basic_level True))
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
