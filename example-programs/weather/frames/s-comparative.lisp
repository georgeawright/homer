(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define location-concept-1
  (def-concept :name "" :is_slot True :parent_space location-space))
(define location-concept-2
  (def-concept :name "" :is_slot True :parent_space location-space))
(define label-parent-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space
    :locations (list (Location (list) conceptual-space))))
(define relation-parent-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :locations (list (Location (list) more-less-space))))
(def-relation :start label-parent-concept :end relation-parent-concept
  :parent_concept more-concept)
(define rp-sub-frame-input
  (def-contextual-space :name "rp-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space conceptual-space)))
(define rp-sub-frame-output
  (def-contextual-space :name "rp-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space conceptual-space)))
(define rp-sub-frame
  (def-sub-frame :name "s-comparative-rp-sub" :parent_concept rp-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet label-parent-concept relation-parent-concept)
    :input_space rp-sub-frame-input
    :output_space rp-sub-frame-output))
(define nn-sub-frame-1-input
  (def-contextual-space :name "nn-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space conceptual-space)))
(define nn-sub-frame-1-output
  (def-contextual-space :name "nn-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space conceptual-space)))
(define nn-sub-frame-1
  (def-sub-frame :name "s-comparative-nn-sub-1" :parent_concept np-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet location-concept-1)
    :input_space nn-sub-frame-1-input
    :output_space nn-sub-frame-1-output))
(define nn-sub-frame-2-input
  (def-contextual-space :name "nn-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space conceptual-space)))
(define nn-sub-frame-2-output
  (def-contextual-space :name "nn-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space conceptual-space)))
(define nn-sub-frame-2
  (def-sub-frame :name "s-comparative-nn-sub-2" :parent_concept np-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet location-concept-2)
    :input_space nn-sub-frame-2-input
    :output_space nn-sub-frame-2-output))
(define comparative-sentence-input
  (def-contextual-space :name "s-comparative.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space conceptual-space)))
(define comparative-sentence-output
  (def-contextual-space :name "s-comparative.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space location-space conceptual-space)))
(define comparative-sentence
  (def-frame :name "s-comparative" :parent_concept sentence-concept :parent_frame None
    :depth 6
    :sub_frames (StructureSet rp-sub-frame nn-sub-frame-1 nn-sub-frame-2)
    :concepts (StructureSet
	       label-parent-concept relation-parent-concept location-concept-1 location-concept-2)
    :input_space comparative-sentence-input
    :output_space comparative-sentence-output))
(define chunk-start
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) conceptual-space)
			      (Location (list) nn-sub-frame-1-input)
			      (Location (list) rp-sub-frame-input)
			      (Location (list) comparative-sentence-input))
    :parent_space nn-sub-frame-1-input))
(define chunk-end
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) conceptual-space)
			      (Location (list) nn-sub-frame-2-input)
			      (Location (list) rp-sub-frame-input)
			      (Location (list) comparative-sentence-input))
    :parent_space nn-sub-frame-2-input))
(define chunk-start-conceptual-label
  (def-label :start chunk-start :parent_concept label-parent-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) rp-sub-frame-input)
		     (Location (list) comparative-sentence-input))
    :parent_space rp-sub-frame-input))
(define chunk-start-location-label
  (def-label :start chunk-start :parent_concept location-concept-1
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-sub-frame-1-input)
		     (Location (list) comparative-sentence-input))))
(define chunk-end-location-label
  (def-label :start chunk-end :parent_concept location-concept-2
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-sub-frame-2-input)
		     (Location (list) comparative-sentence-input))))
(define relation
  (def-relation :start chunk-start :end chunk-end :parent_concept relation-parent-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list) (list) conceptual-space)
		     (TwoPointLocation (list) (list) rp-sub-frame-input)
		     (TwoPointLocation (list) (list) comparative-sentence-input))
    :parent_space rp-sub-frame-input
    :conceptual_space conceptual-space))
(define sentence-word-1
  (def-letter-chunk :name "temperatures"
    :locations (list nsubj-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-1-label
  (def-label :start sentence-word-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) comparative-sentence-output))))
(define sentence-word-2
  (def-letter-chunk :name "will"
    :locations (list vb-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk will))
(define sentence-word-3
  (def-letter-chunk :name "be"
    :locations (list cop-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk be))
(define sentence-word-4
  (def-letter-chunk :name None
    :locations (list rp-location
		     (Location (list) rp-sub-frame-output)
		     (Location (list) comparative-sentence-output))
    :parent_space rp-sub-frame-output))
(define jjr-chunk-grammar-label
  (def-label :start sentence-word-4 :parent_concept rp-concept
    :locations (list rp-location
		     (Location (list) rp-sub-frame-output))))
(define sentence-word-5
  (def-letter-chunk :name "in"
    :locations (list prep-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk in))
(define sentence-word-6
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk the))
(define sentence-word-7
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-sub-frame-1-output)
		     (Location (list) comparative-sentence-output))
    :parent_space nn-sub-frame-1-output))
(define nn-1-grammar-label
  (def-label :start sentence-word-7 :parent_concept np-concept
    :locations (list np-location
		     (Location (list) nn-sub-frame-1-output))))
(define sentence-word-8
  (def-letter-chunk :name "than"
    :locations (list prep-location
		     (Location (list) comparative-sentence-output))
    :abstract_chunk than))
(define sentence-word-9
  (def-letter-chunk :name "in"
    :locations (list prep-location
		     (Location (list) comparative-sentence-output))
    :abstract_chunk in))
(define sentence-word-10
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) comparative-sentence-output))
    :abstract_chunk the))
(define sentence-word-11
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-sub-frame-2-output)
		     (Location (list) comparative-sentence-output))
    :parent_space nn-sub-frame-2-output))
(define nn-2-chunk-grammar-label
  (def-label :start sentence-word-11 :parent_concept np-concept
    :locations (list np-location
		     (Location (list) nn-sub-frame-2-output))))
(define vb-super-chunk
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-2)
    :right_branch (StructureSet sentence-word-3)))
(define vb-super-chunk-label
  (def-label :start vb-super-chunk :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) comparative-sentence-output))))
(define np-1-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-6)
    :right_branch (StructureSet sentence-word-7)))
(define np-2-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-10)
    :right_branch (StructureSet sentence-word-11)))
(define pp-1-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-5)
    :right_branch (StructureSet np-1-super-chunk)))
(define pp-2-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-9)
    :right_branch (StructureSet np-2-super-chunk)))
(define rp-super-chunk
  (def-letter-chunk :name None
    :locations (list rp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-4)
    :right_branch (StructureSet pp-1-super-chunk)))
(define comp-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-8)
    :right_branch (StructureSet pp-2-super-chunk)))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet rp-super-chunk)
    :right_branch (StructureSet comp-super-chunk)))
(define pred-super-chunk-label
   (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) comparative-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet vb-super-chunk)
    :right_branch (StructureSet pred-super-chunk)))
(define vp-super-chunk-label
   (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) comparative-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :left_branch (StructureSet sentence-word-1)
    :right_branch (StructureSet vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) comparative-sentence-output))))

(def-relation :start label-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start relation-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start nn-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start jj-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start jjr-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start rp-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start sentence-concept :end comparative-sentence
  :is_bidirectional True :activation 1.0)
