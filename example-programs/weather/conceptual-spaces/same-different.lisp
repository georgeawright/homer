(define same-different-concept
  (def-concept :name "same-different" :locations (list) :classifier None :instance_type None
    :structure_type Correspondence :parent_space None
    :distance_function centroid_euclidean_distance))
(define same-different-space
  (def-conceptual-space :name "same-different" :parent_concept same-different-concept
    :no_of_dimensions 1))
(define same-concept
  (def-concept :name "same"
    :locations (list (Location (list (list 10)) same-different-space))
    :classifier (SamenessClassifier) :instance_type Chunk :structure_type Correspondence
    :parent_space same-different-space :distance_function centroid_euclidean_distance))
(define not-same-concept
  (def-compound-concept :root not-concept :args (list same-concept)))
(define different-concept
  (def-concept :name "different"
    :locations (list (Location (list (list 10)) same-different-space))
    :classifier (DifferentnessClassifier) :instance_type Chunk :structure_type Correspondence
    :parent_space same-different-space :distance_function centroid_euclidean_distance))
(define not-different-concept
  (def-compound-concept :root not-concept :args (list different-concept)))

(define same-word (def-letter-chunk :name "same" :locations (list)))
(def-relation :start same-concept :end same-word :parent_concept jj-concept)
(define different-word (def-letter-chunk :name "different" :locations (list)))
(def-relation :start different-concept :end different-word :parent_concept jj-concept)

