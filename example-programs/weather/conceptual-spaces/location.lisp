(define location-dist-to-prox-weight 1)
(define location-concept
  (def-concept :name "location" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function area_euclidean_distance :activation 1.0
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define north-south-space
  (def-conceptual-space :name "north-south" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[c[0]] for c in location.coordinates]
"""))))))
(define west-east-space
  (def-conceptual-space :name "west-east" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[c[1]] for c in location.coordinates]
"""))))))
(define nw-se-space
  (def-conceptual-space :name "northwest-southeast" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[sum(c)/len(c)] for c in location.coordinates]
"""))))))
(define ne-sw-space
  (def-conceptual-space :name "northeast-southwest" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[(c[0]+8-c[1])/2] for c in location.coordinates]
"""))))))
(define location-space
  (def-conceptual-space :name "location" :parent_concept location-concept
    :no_of_dimensions 2
    :dimensions (list north-south-space west-east-space)
    :sub_spaces (list north-south-space west-east-space nw-se-space ne-sw-space)
    :is_basic_level True))
(define north-concept
  (def-concept :name "north" :locations (list (Location (list (list 0 4)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space north-south-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define south-concept
  (def-concept :name "south" :locations (list (Location (list (list 8 4)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space north-south-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define west-concept
  (def-concept :name "west" :locations (list (Location (list (list 4 0)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space west-east-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define east-concept
  (def-concept :name "east" :locations (list (Location (list (list 4 8)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space west-east-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define northwest-concept
  (def-concept :name "northwest" :locations (list (Location (list (list 0 0)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space nw-se-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define northeast-concept
  (def-concept :name "northeast" :locations (list (Location (list (list 0 8)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space ne-sw-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define southwest-concept
  (def-concept :name "southwest" :locations (list (Location (list (list 8 0)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space ne-sw-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define southeast-concept
  (def-concept :name "southeast" :locations (list (Location (list (list 8 8)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space nw-se-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define central-concept
  (def-concept :name "central"
    :locations (list (Location (list (list 4 4)) location-space)
		     (Location (list (list 0)) peripheralness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space peripheralness-space :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))
(define everywhere-concept
  (def-concept :name "everywhere"
    :locations (list (Location
		      (list (list 0 0) (list 0 8) (list 8 0) (list 8 8) (list 4 4))
		      location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function area_euclidean_distance
    :distance_to_proximity_weight location-dist-to-prox-weight))

(def-relation :start north-concept :end more-concept
  :parent_concept more-concept :activation 1.0)
(def-relation :start west-concept :end more-concept
  :parent_concept more-concept :activation 1.0)
(def-relation :start northeast-concept :end more-concept
  :parent_concept more-concept :activation 1.0)
(def-relation :start northwest-concept :end more-concept
  :parent_concept more-concept :activation 1.0)

(def-relation :start south-concept :end less-concept
  :parent_concept more-concept :activation 1.0)
(def-relation :start east-concept :end less-concept
  :parent_concept more-concept :activation 1.0)
(def-relation :start southwest-concept :end less-concept
  :parent_concept more-concept :activation 1.0)
(def-relation :start southeast-concept :end less-concept
  :parent_concept more-concept :activation 1.0)

(define north-word
  (def-letter-chunk :name "north" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 0 4)) location-space))))
(def-relation :start north-concept :end north-word :parent_concept nn-concept)
(def-relation :start north-concept :end north-word :parent_concept pp-allative-concept)
(def-relation :start north-word :end -wards :parent_concept pp-allative-concept)
(define south-word
  (def-letter-chunk :name "south" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 10 4)) location-space))))
(def-relation :start south-concept :end south-word :parent_concept nn-concept)
(def-relation :start south-concept :end south-word :parent_concept pp-allative-concept)
(def-relation :start south-word :end -wards :parent_concept pp-allative-concept)
(define west-word
  (def-letter-chunk :name "west" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 5 0)) location-space))))
(def-relation :start west-concept :end west-word :parent_concept nn-concept)
(def-relation :start west-concept :end west-word :parent_concept pp-allative-concept)
(def-relation :start west-word :end -wards :parent_concept pp-allative-concept)
(define east-word
  (def-letter-chunk :name "east" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 5 8)) location-space))))
(def-relation :start east-concept :end east-word :parent_concept nn-concept)
(def-relation :start east-concept :end east-word :parent_concept pp-allative-concept)
(def-relation :start east-word :end -wards :parent_concept pp-allative-concept)
(define northwest-word
  (def-letter-chunk :name "northwest" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 0 0)) location-space))))
(def-relation :start northwest-concept :end northwest-word :parent_concept nn-concept)
(def-relation :start northwest-concept :end northwest-word :parent_concept pp-allative-concept)
(def-relation :start northwest-word :end -wards :parent_concept pp-allative-concept)
(define northeast-word
  (def-letter-chunk :name "northeast" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 0 8)) location-space))))
(def-relation :start northeast-concept :end northeast-word :parent_concept nn-concept)
(def-relation :start northeast-concept :end northeast-word :parent_concept pp-allative-concept)
(def-relation :start northeast-word :end -wards :parent_concept pp-allative-concept)
(define southwest-word
  (def-letter-chunk :name "southwest" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 10 0)) location-space))))
(def-relation :start southwest-concept :end southwest-word :parent_concept nn-concept)
(def-relation :start southwest-concept :end southwest-word :parent_concept pp-allative-concept)
(def-relation :start southwest-word :end -wards :parent_concept pp-allative-concept)
(define southeast-word
  (def-letter-chunk :name "southeast" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 10 8)) location-space))))
(def-relation :start southeast-concept :end southeast-word :parent_concept nn-concept)
(def-relation :start southeast-concept :end southeast-word :parent_concept pp-allative-concept)
(def-relation :start southeast-word :end -wards :parent_concept pp-allative-concept)
(define centre-word
  (def-letter-chunk :name "centre" :parent_space peripheralness-space
    :locations (list (Location (list) grammar-space))))
(def-relation :start central-concept :end centre-word :parent_concept nn-concept)
(define midlands-word
  (def-letter-chunk :name "midlands" :parent_space peripheralness-space
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 5 4)) location-space)
		     (Location (list (list 0)) peripheralness-space))))
(def-relation :start central-concept :end midlands-word :parent_concept nn-concept)
(define country-word
  (def-letter-chunk :name "country" :parent_space location-space
    :locations (list (Location (list) grammar-space)
		     (Location
		      (list (list 0 0) (list 0 8) (list 8 0) (list 8 8) (list 4 4))
		      location-space))))
(def-relation :start everywhere-concept :end country-word :parent_concept nn-concept)

(def-relation :start north-concept :end south-concept
  :parent_concept more-concept :quality 1.0)
(def-relation :start west-concept :end east-concept
  :parent_concept more-concept :quality 1.0)
(def-relation :start northwest-concept :end southeast-concept
  :parent_concept more-concept :quality 1.0)
(def-relation :start northeast-concept :end southwest-concept
  :parent_concept more-concept :quality 1.0)

(def-relation :start south-concept :end north-concept
  :parent_concept less-concept :quality 1.0)
(def-relation :start east-concept :end west-concept
  :parent_concept less-concept :quality 1.0)
(def-relation :start southeast-concept :end northwest-concept
  :parent_concept less-concept :quality 1.0)
(def-relation :start southwest-concept :end northeast-concept
  :parent_concept more-concept :quality 1.0)

(def-relation :start northwest-concept :end north-concept :is_excitatory False :quality 1.0)
(def-relation :start northwest-concept :end west-concept :is_excitatory False :quality 1.0)
(def-relation :start northeast-concept :end north-concept :is_excitatory False :quality 1.0)
(def-relation :start northeast-concept :end east-concept :is_excitatory False :quality 1.0)
(def-relation :start southwest-concept :end south-concept :is_excitatory False :quality 1.0)
(def-relation :start southwest-concept :end west-concept :is_excitatory False :quality 1.0)
(def-relation :start southeast-concept :end south-concept :is_excitatory False :quality 1.0)
(def-relation :start southeast-concept :end east-concept :is_excitatory False :quality 1.0)
