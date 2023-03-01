(define temperature-dist-to-prox-weight 2)
(define temperature-concept
  (def-concept :name "temperature" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight temperature-dist-to-prox-weight))
(define temperature-space
  (def-conceptual-space :name "temperature" :parent_concept temperature-concept
    :breadth 2 :no_of_dimensions 1 :is_basic_level True
    :dimensions (list) :sub_spaces (list extremeness-space)))
(define hot-concept
  (def-concept :name "hot" :locations (list (Location (list (list 22)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space temperature-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight temperature-dist-to-prox-weight))
(define warm-concept
  (def-concept :name "warm" :locations (list (Location (list (list 18)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space temperature-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight temperature-dist-to-prox-weight))
(define mild-concept
  (def-concept :name "mild"
    :locations (list (Location (list (list 0)) extremeness-space)
		     (Location (list (list 13)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space extremeness-space :distance_function centroid_euclidean_distance))
(define cool-concept
  (def-concept :name "cool" :locations (list (Location (list (list 8)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space temperature-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight temperature-dist-to-prox-weight))
(define cold-concept
  (def-concept :name "cold" :locations (list (Location (list (list 4)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space temperature-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight temperature-dist-to-prox-weight))

(def-relation :start hot-concept :end more-concept :parent_concept more-concept :quality 1.0)
(def-relation :start warm-concept :end more-concept :parent_concept more-concept :quality 1.0)
(def-relation :start extreme-concept :end more-concept :parent_concept more-concept :quality 1.0)
(def-relation :start cool-concept :end less-concept :parent_concept more-concept :quality 1.0)
(def-relation :start cold-concept :end less-concept :parent_concept more-concept :quality 1.0)
(def-relation :start mild-concept :end less-concept :parent_concept more-concept :quality 1.0)

(def-correspondence :start hot-concept :end high-concept :parent_concept same-concept)
(def-correspondence :start hot-concept :end good-concept :parent_concept same-concept)
(def-correspondence :start cold-concept :end low-concept :parent_concept same-concept)
(def-correspondence :start cold-concept :end bad-concept :parent_concept same-concept)

(define hot-word
  (def-letter-chunk :name "hot" :parent_space temperature-space
    :locations (list (Location (list (list 22)) temperature-space))))
(def-relation :start hot-concept :end hot-word :parent_concept jj-concept)
(define hott-word
  (def-letter-chunk :name "hott" :parent_space temperature-space
    :locations (list (Location (list (list 22)) temperature-space))))
(def-relation :start hot-concept :end hott-word :parent_concept jjr-concept)
(def-relation :start hott-word :end -er :parent_concept jjr-concept)
(define heat-word
  (def-letter-chunk :name "heat" :parent_space temperature-space
    :locations (list (Location (list (list 22)) temperature-space))))
(def-relation :start hot-concept :end heat-word :parent_concept nn-concept)
(define warm-word
  (def-letter-chunk :name "warm" :parent_space temperature-space
    :locations (list (Location (list (list 18)) temperature-space))))
(def-relation :start warm-concept :end warm-word :parent_concept jj-concept)
(def-relation :start warm-concept :end warm-word :parent_concept jjr-concept)
(def-relation :start warm-word :end -er :parent_concept jjr-concept)
(define warmth-word
  (def-letter-chunk :name "warmth" :parent_space temperature-space
    :locations (list (Location (list (list 18)) temperature-space))))
(def-relation :start warm-concept :end warmth-word :parent_concept nn-concept)
(define cool-word
  (def-letter-chunk :name "cool" :parent_space temperature-space
    :locations (list (Location (list (list 8)) temperature-space))))
(def-relation :start cool-concept :end cool-word :parent_concept jj-concept)
(def-relation :start cool-concept :end cool-word :parent_concept jjr-concept)
(def-relation :start cool-word :end -er :parent_concept jjr-concept)
(define cold-word
  (def-letter-chunk :name "cold" :parent_space temperature-space
    :locations (list (Location (list (list 4)) temperature-space))))
(def-relation :start cold-concept :end cold-word :parent_concept jj-concept)
(def-relation :start cold-concept :end cold-word :parent_concept jjr-concept)
(def-relation :start cold-word :end -er :parent_concept jjr-concept)

(define mild-word
  (def-letter-chunk :name "mild" :parent_space extremeness-space
    :locations (list (Location (list (list 0)) extremeness-space))))
(def-relation :start mild-concept :end mild-word :parent_concept jj-concept)
(def-relation :start mild-concept :end mild-word :parent_concept jjr-concept)
(def-relation :start mild-word :end -er :parent_concept jjr-concept)
(define extreme-word
  (def-letter-chunk :name "extreme" :parent_space extremeness-space
    :locations (list (Location (list (list 10)) extremeness-space))))
(def-relation :start extreme-concept :end extreme-word :parent_concept jj-concept)

(define same-temperature-concept (def-concept :name "same-temperature"))
(def-relation :start same-concept :end same-temperature-concept
  :parent_concept temperature-concept)
(define different-temperature-concept (def-concept :name "different-temperature"))
(def-relation :start different-concept :end different-temperature-concept
  :parent_concept temperature-concept)
(define more-temperature-concept (def-concept :name "more-temperature"))
(def-relation :start more-concept :end more-temperature-concept
  :parent_concept temperature-concept)
(define less-temperature-concept (def-concept :name "less-temperature"))
(def-relation :start less-concept :end less-temperature-concept
  :parent_concept temperature-concept)
