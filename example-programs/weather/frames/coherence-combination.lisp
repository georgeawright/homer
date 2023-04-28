(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet location-space
				      time-space
				      temperature-space
				      height-space
				      goodness-space)
    :no_of_dimensions Nan))
(define location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define comparison-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :possible_instances (StructureSet more-concept less-concept)
    :locations (list (Location (list) more-less-space))))
 
(define combination-sub-1-input
  (def-contextual-space :name "combination-sub-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define combination-sub-1-output
  (def-contextual-space :name "combination-sub-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define combination-sub-1
  (def-sub-frame :name "combination-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space combination-sub-1-input
    :output_space combination-sub-1-output))
(define combination-sub-2-input
  (def-contextual-space :name "combination-sub-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define combination-sub-2-output
  (def-contextual-space :name "combination-sub-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define combination-sub-2
  (def-sub-frame :name "combination-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space combination-sub-2-input
    :output_space combination-sub-2-output))

(define combination-input
  (def-contextual-space :name "combination.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet)))
(define combination-output
  (def-contextual-space :name "combination.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space)))
(define combination
  (def-frame :name "combination" :parent_concept conjunction-concept :parent_frame None
    :depth 8
    :sub_frames (StructureSet combination-sub-1 combination-sub-2)
    :concepts (StructureSet)
    :input_space combination-input
    :output_space combination-output))

(define sentence-1
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) combination-sub-1-output)
		     (Location (list) combination-output))
    :parent_space combination-sub-1-output))
(define sentence-1-sentence-label
  (def-label :start sentence-1 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) combination-sub-1-output))))
(define sentence-2
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) combination-sub-1-output)
		     (Location (list) combination-output))
    :parent_space combination-sub-1-output))
(define sentence-2-sentence-label
  (def-label :start sentence-2 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) combination-sub-1-output))))
(define sentence-3
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) combination-sub-2-output)
		     (Location (list) combination-output))
    :parent_space combination-sub-2-output))
(define sentence-3-sentence-label
  (def-label :start sentence-3 :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) combination-sub-2-output))))
(define sentence-4
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) combination-sub-2-output)
		     (Location (list) combination-output))
    :parent_space combination-sub-2-output))
(define sentence-4-sentence-label
  (def-label :start sentence-4 :parent_concept sentence-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) combination-sub-2-output))))
(define relation-1-3
  (def-relation :start sentence-1 :end sentence-3 :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) string-space)
		     (TwoPointLocation (list) (list) combination-output))
    :is_interspatial True
    :parent_space None
    :conceptual_space string-space))
(define relation-2-4
  (def-relation :start sentence-2 :end sentence-4 :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) string-space)
		     (TwoPointLocation (list) (list) combination-output))
    :is_interspatial True
    :parent_space None
    :conceptual_space string-space))
((getattr (getattr combination "interspatial_links") "add") relation-1-3)
((getattr (getattr combination "interspatial_links") "add") relation-2-4)

(define conj-word-1
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) combination-sub-1-output)
		     (Location (list) combination-output))
    :parent_space combination-sub-1-output))
(define conj-word-2
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) combination-sub-2-output)
		     (Location (list) combination-output))
    :parent_space combination-sub-2-output))
(define conj-relation
  (def-relation :start conj-word-1 :end conj-word-2 :parent_concept more-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) grammar-space)
		     (TwoPointLocation (list) (list) combination-output))
    :is_interspatial True
    :parent_space None
    :conceptual_space grammar-space))
(define conj-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) combination-sub-2-output)
		     (Location (list) combination-output))
    :left_branch (StructureSet conj-word-1)
    :right_branch (StructureSet conj-word-2)
    :parent_space combination-output))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) combination-output))
    :left_branch (StructureSet conj-super-chunk)
    :right_branch (StructureSet sentence-4)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) combination-output))
    :left_branch (StructureSet sentence-3)
    :right_branch (StructureSet conjunction-super-chunk)))

(def-relation :start conjunction-concept :end combination
  :is_bidirectional True :stable_activation 1.0)

