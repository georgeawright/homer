(define time-concept
  (def-concept :name "time" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define time-space
  (def-conceptual-space :name "time" :parent_concept time-concept
    :no_of_dimensions 1 :is_basic_level True))
(define friday-concept
  (def-concept :name "friday" :locations (list (Location (list (list 0)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function centroid_euclidean_distance))
(define saturday-concept
  (def-concept :name "saturday" :locations (list (Location (list (list 1)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function centroid_euclidean_distance))
(define sunday-concept
  (def-concept :name "sunday" :locations (list (Location (list (list 2)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function centroid_euclidean_distance))

(def-correspondence :start friday-concept :end early-concept :parent_concept same-concept)
(def-correspondence :start sunday-concept :end late-concept :parent_concept same-concept)

(define friday-word
  (def-letter-chunk :name "friday" :parent_space time-space
    :locations (list (Location (list (list 0)) time-space))))
(def-relation :start friday-concept :end friday-word :parent_concept nn-concept)
(define saturday-word
  (def-letter-chunk :name "saturday" :parent_space time-space
    :locations (list (Location (list (list 1)) time-space))))
(def-relation :start saturday-concept :end saturday-word :parent_concept nn-concept)
(define sunday-word
  (def-letter-chunk :name "sunday" :parent_space time-space
    :locations (list (Location (list (list 2)) time-space))))
(def-relation :start sunday-concept :end sunday-word :parent_concept nn-concept)
