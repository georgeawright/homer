(define time-concept
  (def-concept :name "time" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function boolean_distance))
(define time-space
  (def-conceptual-space :name "time" :parent_concept time-concept
    :no_of_dimensions 1 :is_basic_level True))
(define friday-concept
  (def-concept :name "friday" :locations (list (Location (list (list 0)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))
(define saturday-concept
  (def-concept :name "saturday" :locations (list (Location (list (list 24)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))
(define sunday-concept
  (def-concept :name "sunday" :locations (list (Location (list (list 48)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))
(define always-concept
  (def-concept :name "always"
    :locations (list (Location (list (list 0) (list 24) (list 48)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function area_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))

(def-correspondence :start friday-concept :end early-concept :parent_concept same-concept)
(def-correspondence :start sunday-concept :end late-concept :parent_concept same-concept)

(define friday-word
  (def-letter-chunk :name "friday" :parent_space time-space
    :locations (list (Location (list (list 0)) time-space))))
(def-relation :start friday-concept :end friday-word :parent_concept nn-concept)
(define saturday-word
  (def-letter-chunk :name "saturday" :parent_space time-space
    :locations (list (Location (list (list 24)) time-space))))
(def-relation :start saturday-concept :end saturday-word :parent_concept nn-concept)
(define sunday-word
  (def-letter-chunk :name "sunday" :parent_space time-space
    :locations (list (Location (list (list 48)) time-space))))
(def-relation :start sunday-concept :end sunday-word :parent_concept nn-concept)
(define everyday-word
  (def-letter-chunk :name "everyday" :parent_space time-space
    :locations (list (Location (list (list 0) (list 24) (list 48)) time-space))))
(def-relation :start always-concept :end everyday-word :parent_concept nn-concept)
(define throughout-the-weekend-phrase
  (def-letter-chunk :name "throughout~the~weekend" :parent_space time-space
    :locations (list (Location (list (list 0) (list 24) (list 48)) time-space))))
(def-relation
  :start always-concept :end throughout-the-weekend-phrase :parent_concept pp-concept)

(define same-time-concept (def-concept :name "same-time"))
(def-relation :start same-concept :end same-time-concept
  :parent_concept time-concept)
(define different-time-concept (def-concept :name "different-time"))
(def-relation :start different-concept :end different-time-concept
  :parent_concept time-concept)
(define more-time-concept (def-concept :name "more-time"))
(def-relation :start more-concept :end more-time-concept
  :parent_concept time-concept)
(define less-time-concept (def-concept :name "less-time"))
(def-relation :start less-concept :end less-time-concept
  :parent_concept time-concept)
