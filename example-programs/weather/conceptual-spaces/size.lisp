(define size-concept
  (def-concept :name "size" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define size-space
  (def-conceptual-space :name "size" :parent_concept size-concept
    :no_of_dimensions 1 :is_basic_level True))
(define large-concept
  (def-concept :name "large" :locations (list (Location (list (list 10)) size-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space size-space :distance_function centroid_euclidean_distance))
(define medium-concept
  (def-concept :name "medium" :locations (list (Location (list (list 7)) size-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space size-space :distance_function centroid_euclidean_distance))
(define small-concept
  (def-concept :name "small" :locations (list (Location (list (list 4)) size-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space size-space :distance_function centroid_euclidean_distance))
(define tiny-concept
  (def-concept :name "tiny" :locations (list (Location (list (list 1)) size-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space size-space :distance_function centroid_euclidean_distance))

(def-relation :start large-concept :end more-concept :parent_concept more-concept :quality 1.0)
(def-relation :start medium-concept :end more-concept :parent_concept more-concept :quality 1.0)
(def-relation :start small-concept :end less-concept :parent_concept more-concept :quality 1.0)
(def-relation :start tiny-concept :end less-concept :parent_concept more-concept :quality 1.0)

(define large-word
  (def-letter-chunk :name "large" :parent_space size-space
    :locations (list (Location (list (list 10)) size-space))))
(def-relation :start large-concept :end large-word :parent_concept jj-concept)
(define larg-word
  (def-letter-chunk :name "larg" :parent_space size-space
    :locations (list (Location (list (list 10)) size-space))))
(def-relation :start large-concept :end larg-word :parent_concept jjr-concept)
(def-relation :start larg-word :end -er :parent_concept jjr-concept)
(define medium-word
  (def-letter-chunk :name "medium" :parent_space size-space
    :locations (list (Location (list (list 7)) size-space))))
(def-relation :start medium-concept :end medium-word :parent_concept jj-concept)
(define expand-word
  (def-letter-chunk :name "expand" :parent_space size-space
    :locations (list vb-location expand-location (Location (list (list 10)) size-space))))
(def-relation :start large-concept :end expand-word :parent_concept vb-concept)
(def-relation :start medium-concept :end expand-word :parent_concept vb-concept)

(define small-word
  (def-letter-chunk :name "small" :parent_space size-space
    :locations (list (Location (list (list 4)) size-space))))
(def-relation :start small-concept :end small-word :parent_concept jj-concept)
(def-relation :start small-concept :end small-word :parent_concept jjr-concept)
(def-relation :start small-word :end -er :parent_concept jjr-concept)
(define tiny-word
  (def-letter-chunk :name "tiny" :parent_space size-space
    :locations (list (Location (list (list 1)) size-space))))
(def-relation :start tiny-concept :end tiny-word :parent_concept jj-concept)
(define tini-word
  (def-letter-chunk :name "tini" :parent_space size-space
    :locations (list (Location (list (list 1)) size-space))))
(def-relation :start tiny-concept :end tini-word :parent_concept jjr-concept)
(def-relation :start tini-word :end -er :parent_concept jjr-concept)
(define shrink-word
  (def-letter-chunk :name "shrink" :parent_space size-space
    :locations (list vb-location shrink-location (Location (list (list 1)) size-space))))
(def-relation :start small-concept :end shrink-word :parent_concept vb-concept)
(def-relation :start tiny-concept :end shrink-word :parent_concept vb-concept)

(def-relation :start expand-word :end shrink-word :parent_concept opposite-concept)
(def-relation :start shrink-word :end expand-word :parent_concept opposite-concept)
(def-relation :start large-word :end small-word :parent_concept opposite-concept)
(def-relation :start small-word :end large-word :parent_concept opposite-concept)

(define same-size-concept (def-concept :name "same-size"))
(def-relation :start same-concept :end same-size-concept
  :parent_concept size-concept)
(define different-size-concept (def-concept :name "different-size"))
(def-relation :start different-concept :end different-size-concept
  :parent_concept size-concept)
(define more-size-concept (def-concept :name "more-size"))
(def-relation :start more-concept :end more-size-concept
  :parent_concept size-concept)
(define less-size-concept (def-concept :name "less-size"))
(def-relation :start less-concept :end less-size-concept
  :parent_concept size-concept)
