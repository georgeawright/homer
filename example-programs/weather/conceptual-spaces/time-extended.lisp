(define time-concept
  (def-concept :name "time" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function boolean_distance))
(define time-space
  (def-conceptual-space :name "time" :parent_concept time-concept
    :no_of_dimensions 1 :is_basic_level True))
(define monday-concept
  (def-concept :name "monday" :locations (list (Location (list (list 0)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))
(define tuesday-concept
  (def-concept :name "tuesday" :locations (list (Location (list (list 24)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))
(define wednesday-concept
  (def-concept :name "wednesday" :locations (list (Location (list (list 48)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))
(define thursday-concept
  (def-concept :name "thursday" :locations (list (Location (list (list 72)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))
(define friday-concept
  (def-concept :name "friday" :locations (list (Location (list (list 96)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance))
(define always-concept
  (def-concept :name "always"
    :locations (list (Location (list (list 0) (list 24) (list 48) (list 72) (list 96)) time-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space time-space :distance_function boolean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))

(def-correspondence :start monday-concept :end early-concept :parent_concept same-concept)
(def-correspondence :start friday-concept :end late-concept :parent_concept same-concept)

(define monday-word
  (def-letter-chunk :name "monday" :parent_space time-space
    :locations (list nn-location (Location (list (list 0)) time-space))))
(def-relation :start monday-concept :end monday-word :parent_concept nn-concept)
(define tuesday-word
  (def-letter-chunk :name "tuesday" :parent_space time-space
    :locations (list nn-location (Location (list (list 24)) time-space))))
(def-relation :start tuesday-concept :end tuesday-word :parent_concept nn-concept)
(define wednesday-word
  (def-letter-chunk :name "wednesday" :parent_space time-space
    :locations (list nn-location (Location (list (list 48)) time-space))))
(def-relation :start wednesday-concept :end wednesday-word :parent_concept nn-concept)
(define thursday-word
  (def-letter-chunk :name "thursday" :parent_space time-space
    :locations (list nn-location (Location (list (list 72)) time-space))))
(def-relation :start thursday-concept :end thursday-word :parent_concept nn-concept)
(define friday-word
  (def-letter-chunk :name "friday" :parent_space time-space
    :locations (list nn-location (Location (list (list 96)) time-space))))
(def-relation :start friday-concept :end friday-word :parent_concept nn-concept)
(define everyday-word
  (def-letter-chunk :name "everyday" :parent_space time-space
    :locations (list nn-location (Location (list (list 0) (list 24) (list 48) (list 72) (list 96)) time-space))))
(def-relation :start always-concept :end everyday-word :parent_concept nn-concept)
(define throughout-the-week-phrase
  (def-letter-chunk :name "throughout~the~week" :parent_space time-space
    :locations (list (Location (list (list 0) (list 24) (list 48) (list 72) (list 96)) time-space))))
(def-relation
  :start always-concept :end throughout-the-week-phrase :parent_concept pp-concept)

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

(define less-time-cross_view-concept (def-concept :name "less-time-cross_view"))
(def-relation :start less-time-concept :end less-time-cross_view-concept
  :parent_concept outer-concept)
(define same-time-cross_view-concept (def-concept :name "samw-time-cross_view"))
(def-relation :start same-time-concept :end same-time-cross_view-concept
  :parent_concept outer-concept)

