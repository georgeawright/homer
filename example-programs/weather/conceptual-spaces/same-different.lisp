(define same-different-concept
  (def-concept :name "same-different" :locations (list) :classifier None :instance_type None
    :structure_type Relation :parent_space None
    :distance_function centroid_euclidean_distance))
(define same-different-space
  (def-conceptual-space :name "same-different" :parent_concept same-different-concept
    :no_of_dimensions 1))
(define same-concept
  (def-concept :name "same"
    :locations (list (Location (list (list 10)) same-different-space))
    :classifier (SamenessClassifier) :instance_type Chunk :structure_type Relation
    :parent_space same-different-space :distance_function centroid_euclidean_distance))
(setattr same-concept "reverse" same-concept)
(define different-concept
  (def-concept :name "different"
    :locations (list (Location (list (list 10)) same-different-space))
    :classifier (DifferentnessClassifier) :instance_type Chunk :structure_type Relation
    :subsumes (StructureSet more-concept less-concept)
    :parent_space same-different-space :distance_function centroid_euclidean_distance))
(setattr different-concept "reverse" different-concept)

(define same-word (def-letter-chunk :name "same" :locations (list)))
(def-relation :start same-concept :end same-word :parent_concept jj-concept)
(define different-word (def-letter-chunk :name "different" :locations (list)))
(def-relation :start different-concept :end different-word :parent_concept jj-concept)

(define same-cross_view-concept (def-concept :name "same-cross_view"))
(def-relation :start same-concept :end same-cross_view-concept
  :parent_concept outer-concept)
(define different-cross_view-concept (def-concept :name "different-cross_view"))
(def-relation :start different-concept :end different-cross_view-concept
  :parent_concept outer-concept)

(define same-verb-concept (def-concept :name "same-verb"))
(def-relation :start same-concept :end same-verb-concept
  :parent_concept vb-concept)
(define same-verb-cross_view-concept (def-concept :name "same-verb-cross_view"))
(def-relation :start same-verb-concept :end same-verb-cross_view-concept
  :parent_concept outer-concept)
